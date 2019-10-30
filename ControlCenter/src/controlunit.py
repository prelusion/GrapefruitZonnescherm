import concurrent
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from serial.serialutil import SerialException

from src import serialinterface as ser
from src import util
from src.decorators import retry_on_any_exception, retry_on_given_exception
from src.models.controlunit import ControlUnitModel

BAUDRATE = 19200

Measurement = namedtuple("SensorData", ["timestamp",
                                        "temperature",
                                        "shutter_status",
                                        "light_sensitivity"])


def get_online_control_units(connected_ports=set(), unused_ports=set()):
    """ :returns new_ports, down_ports """

    @retry_on_given_exception(SerialException, 5)
    def test_if_port_is_control_unit(port):
        with ser.connect(port, baudrate=BAUDRATE, timeout=0.2) as conn:
            for i in range(20):
                conn.write("PING")
                data = conn.readbuffer()

                if "PONG" in data:
                    return port
                time.sleep(0.1)

    all_ports = ser.get_com_ports()
    new_ports = set(all_ports) - set(connected_ports) - set(unused_ports)
    down_ports = set(connected_ports) - set(all_ports) - set(unused_ports)

    unconnected_ports = []
    failed_ports = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures_to_ports = {executor.submit(test_if_port_is_control_unit, port): port for port in new_ports}
        for future in concurrent.futures.as_completed(futures_to_ports):
            port = futures_to_ports[future]
            try:
                result = future.result()
                unconnected_ports.append(result)
            except SerialException as e:
                failed_ports.append(port)

    unconnected_ports = list(filter(None, unconnected_ports))

    invalid_ports = set(all_ports) - set(unconnected_ports) - set(connected_ports) \
                    - set(unused_ports) - set(failed_ports)

    return unconnected_ports, down_ports, invalid_ports


def online_control_unit_service(controlunit_manager, interval=0.5):
    unused_ports = set()

    while True:
        connected_ports = controlunit_manager.get_connected_ports()

        new_ports, down_ports, invalid_ports = get_online_control_units(
            connected_ports=connected_ports, unused_ports=unused_ports)

        unused_ports |= invalid_ports

        for port in down_ports:
            controlunit_manager.remove_unit(port)

        for port in new_ports:

            if controlunit_manager.is_port_connected(port):
                continue

            comm = ControlUnitCommunication(port)

            # TODO: Check for id, otherwise generate id

            model = ControlUnitModel(util.generate_id())

            controlunit_manager.add_unit(port, comm, model)

        time.sleep(interval)


EXCEPT_RETRIES = 5


class ControlUnitCommunication:
    COMMAND_RETRY = 10
    RETRY_SLEEP = 0.2

    def __init__(self, port):
        self.id = None
        self.com_port = port
        self._conn = None

    @retry_on_any_exception(retries=EXCEPT_RETRIES)
    def get_up_time(self):
        return self._get_command("GET_UP_TIME")

    @retry_on_any_exception(retries=EXCEPT_RETRIES)
    def get_id(self):
        return self._get_command("GET_ID")

    def set_id(self, id_):
        """ id is a 32-bit int. """
        return self._set_command("SET_ID", id_)

    def is_online(self):
        pass

    @retry_on_any_exception(retries=EXCEPT_RETRIES)
    def get_sensor_data(self):
        data = self._get_command("GET_LS_THRESHOLD")

        temp, light, shutter = data.split(",")

        return Measurement(
            time.time(), Decimal(temp).quantize(util.QUANTIZE_ONE_DIGIT),
            int(light), int(shutter))

    def get_window_height(self):
        return self._get_command("GET_WINDOW_HEIGHT")

    def set_window_height(self, value):
        return self._set_command("SET_WINDOW_HEIGHT", value)

    def get_temperature_threshold(self):
        return self._get_command("GET_TEMP_THRESHOLD")

    def set_temperature_threshold(self, value):
        return self._set_command("SET_TEMP_THRESHOLD", value)

    def get_light_intensity_threshold(self):
        return self._get_command("GET_LI_THRESHOLD")

    def set_light_intensity_threshold(self, value):
        return self._set_command("SET_LI_THRESHOLD", value)

    def roll_up(self):
        return self._set_command("ROLL_UP")

    def roll_down(self):
        return self._set_command("ROLL_DOWN")

    def get_manual(self):
        return self._get_command("GET_MANUAL")

    def set_manual(self, boolean):
        return self._set_command("SET_MANUAL", boolean)

    @retry_on_any_exception(retries=EXCEPT_RETRIES)
    def _set_command(self, command, arg=None):
        conn = self._get_connection()
        data = None

        cmd_with_arg = command
        if arg:
            cmd_with_arg += "=" + arg

        for i in range(self.COMMAND_RETRY):
            conn.write(cmd_with_arg)
            data = conn.readbuffer()

            if f"{command}=" in data:
                break

            time.sleep(self.RETRY_SLEEP)

        return True if f"{command}=OK" in data else False

    @retry_on_any_exception(retries=EXCEPT_RETRIES)
    def _get_command(self, command):
        conn = self._get_connection()

        for i in range(self.COMMAND_RETRY):
            conn.write(command)
            data = conn.readbuffer()

            if f"{command}=" not in data:
                time.sleep(self.RETRY_SLEEP)
                continue

            return data.split(f"{command}=")[1].strip()

    def _get_connection(self):
        if not self._conn:
            self._conn = ser.Connection(self.com_port, BAUDRATE, timeout=2)
            self._conn.open()
        return self._conn

    def close(self):
        if self._conn: self._conn.close()


if __name__ == "__main__":
    get_online_control_units()
