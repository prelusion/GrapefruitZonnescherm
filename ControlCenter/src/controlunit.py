import time
from collections import namedtuple, OrderedDict
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal

from src import serialinterface as ser
from src import util
from src.decorators import retry_on_except
from src.models.controlunit import ControlUnitModel

BAUDRATE = 38400

Measurement = namedtuple("SensorData", ["timestamp",
                                        "temperature",
                                        "shutter_status",
                                        "light_sensitivity"])


def get_online_control_units(skip=[]):
    """ :returns new_ports, down_ports """

    def test_if_port_is_control_unit(port):
        with ser.connect(port, baudrate=BAUDRATE, timeout=1) as conn:
            for i in range(15):
                conn.write("PING")
                data = conn.readbuffer()
                if "PONG" in data:
                    return port
                time.sleep(0.1)

    all_ports = ser.get_com_ports()
    unconnected_ports = set(all_ports) - set(skip)
    down_ports = set(skip) - set(all_ports)

    with ThreadPoolExecutor() as executor:
        results = executor.map(test_if_port_is_control_unit, unconnected_ports)
        return list(filter(None, results)), down_ports


def online_control_unit_service(controlunit_manager):
    while True:
        connected_ports = controlunit_manager.get_connected_ports()

        new_ports, down_ports = get_online_control_units(skip=connected_ports)

        for port in down_ports:
            controlunit_manager.remove_unit(port)

        for port in new_ports:

            if controlunit_manager.is_port_connected(port):
                continue

            comm = ControlUnitCommunication(port)

            id_ = comm.get_id()
            if not id_:
                comm.set_id(util.generate_id())

            model = ControlUnitModel(id_)

            controlunit_manager.add_unit(port, comm, model)


EXCEPT_RETRIES = 5


class ControlUnitCommunication:
    COMMAND_RETRY = 10
    RETRY_SLEEP = 0.2

    def __init__(self, port):
        self.id = None
        self.com_port = port
        self._conn = None

    @retry_on_except(retries=EXCEPT_RETRIES)
    def get_up_time(self):
        return self._get_command("GET_UP_TIME")

    @retry_on_except(retries=EXCEPT_RETRIES)
    def get_id(self):
        return self._get_command("GET_ID")

    def set_id(self, id_):
        """ id is a 32-bit int. """
        return self._set_command("SET_ID", id_)

    def is_online(self):
        pass

    @retry_on_except(retries=EXCEPT_RETRIES)
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
        return self._get_command("GET_LS_THRESHOLD")

    def set_light_intensity_threshold(self, value):
        return self._set_command("SET_LS_THRESHOLD", value)

    def roll_up(self):
        return self._set_command("ROLL_UP")

    def roll_down(self):
        return self._set_command("ROLL_DOWN")

    def get_manual(self):
        return self._get_command("GET_MANUAL")

    def set_manual(self, boolean):
        return self._set_command("SET_MANUAL", boolean)

    @retry_on_except(retries=EXCEPT_RETRIES)
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

    @retry_on_except(retries=EXCEPT_RETRIES)
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


class ControlUnitManager:
    def __init__(self):
        self._units = OrderedDict()

    def add_unit(self, port, communication, model):
        self._units[port] = (communication, model)

    def remove_unit(self, port):
        del self._units[port]

    def get_units(self):
        return self._units

    def is_port_connected(self, port):
        return port in self._units

    def get_connected_ports(self):
        return list(self._units.keys())

    def update_models(self):
        for i, unit in enumerate(self._units.copy()):
            comm, model = unit

            data = comm.get_sensor_data()

            if not data:
                del self._units[i]

            model.add_measurement(data)

    def close_connections(self):
        for unit in self._units.items():
            comm, model = unit
            comm.close()


if __name__ == "__main__":
    get_online_control_units()
