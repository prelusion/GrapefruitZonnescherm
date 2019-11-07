import concurrent
import threading
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from logging import getLogger

import serial as pyserial
from serial import serialutil

from src import serialinterface as ser
from src import util
from src.decorators import retry_on_any_exception, retry_on_given_exception
from src.models.controlunit import ControlUnitModel

logger = getLogger(__name__)
BAUDRATE = 19200

Measurement = namedtuple("Measurement", ["timestamp",
                                         "temperature",
                                         "shutter_status",
                                         "light_intensity"])


class CommandNotImplemented(Exception):
    pass


def get_online_control_units(connected_ports=set(), unused_ports=set()):
    """ :returns new_ports, down_ports """

    @retry_on_given_exception(SerialException, 5)
    def test_if_port_is_control_unit(port):
        with ser.connect(port, baudrate=BAUDRATE, timeout=0.2) as conn:
            for i in range(20):
                conn.write("PING")
                data = conn.readbuffer()

                if data and "PONG" in data:
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


def online_control_unit_service(app_id, controlunit_manager, interval=0.5):
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

            logger.info(f"control unit connected on port: '{port}'")
            comm = ControlUnitCommunication(port)

            current_id = comm.get_id()
            initialized = True

            if not current_id:
                initialized = False
                unit_id = util.generate_16bit_int()
                current_id = util.encode_controlunit_id(app_id, unit_id)

            logger.info(f"control unit with port '{port}' has id: {current_id}")

            model = ControlUnitModel(current_id)

            model.set_manual(comm.get_manual())
            model.set_online(True)
            model.set_initialized(initialized)

            history = comm.get_sensor_history()
            # TODO do something with sensor history

            controlunit_manager.add_unit(port, comm, model)

        time.sleep(interval)


def sensor_data_service(controlunit_manager, interval):
    while True:
        controlunit_manager.update_sensor_data()
        time.sleep(interval)


EXCEPT_RETRIES = 5


class ControlUnitCommunication:
    COMMAND_RETRY = 4
    BUFFER_READS = 20
    BUFFER_SLEEP = 0.05
    RETRY_SLEEP = 0.1

    def __init__(self, port):
        self.id = None
        self.com_port = port
        self._conn = None

    def initialize(self, device_id, window_height, temperature_threshold, light_intensity_threshold, manual_mode):
        return self._set_command("INITIALIZE",
                                 f"{device_id},{window_height},{temperature_threshold},{light_intensity_threshold},{int(manual_mode)}")

    def get_up_time(self):
        return self._get_command("GET_UP_TIME")

    def get_id(self):
        device_id = self._get_command("GET_ID")
        try:
            if device_id: device_id = int(device_id)
            return device_id
        except ValueError:
            pass

    def set_id(self, id_):
        """ id is a 32-bit int. """
        return self._set_command("SET_ID", str(id_))

    def is_online(self):
        pass

    def get_sensor_data(self):
        data = self._get_command("GET_SENSOR_DATA")

        if not data:
            return

        try:
            temp, light, shutter = data.split(",")
        except ValueError:
            return

        try:
            return Measurement(
                time.time(), Decimal(temp).quantize(util.QUANTIZE_ONE_DIGIT),
                int(shutter), int(light))
        except ValueError:
            return

    def get_sensor_history(self):
        conn = self._get_connection()

        def execute_command():
            conn.readbuffer()  # empty buffer
            conn.write("GET_SENSOR_HISTORY")
            time.sleep(0.1)
            t_start = time.time()
            values = []

            while not util.timeout_exceeded(t_start, 30):
                data = conn.readline()

                if not data:
                    continue

                if "GET_SENSOR_HISTORY=L" in data:
                    datalength = data.split("GET_SENSOR_HISTORY=L")[1].strip()
                elif "GET_SENSOR_HISTORY=OK" in data:
                    return ";".join(values)
                elif "GET_SENSOR_HISTORY=" in data:
                    values.append(data.split("GET_SENSOR_HISTORY=")[1].strip())

        with threading.Lock():
            try:
                history_string = execute_command()
            except (
                    UnicodeDecodeError, Exception, OSError, pyserial.SerialException,
                    serialutil.SerialException) as e:
                logger.exception(e)
                raise pyserial.SerialException

        if not history_string:
            return

        splitted = history_string.split(";")
        splitted.reverse()

        try:
            measurements = []
            for i, value in enumerate(splitted):
                temp, light, shutter = value.split(",")

                measurement = Measurement(
                    time.time() - ((i + 1) * 60), Decimal(temp).quantize(util.QUANTIZE_ONE_DIGIT),
                    int(shutter), int(light))

                measurements.append(measurement)

            measurements.reverse()

            return measurements

        except ValueError:
            pass

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
        value = self._get_command("GET_MANUAL")
        try:
            if value: value = bool(int(value))
            return value
        except ValueError:
            pass

    def set_manual(self, boolean):
        return self._set_command("SET_MANUAL", int(boolean))

    @retry_on_any_exception(retries=EXCEPT_RETRIES)
    def _set_command(self, command, arg=None):
        conn = self._get_connection()

        cmd_with_arg = command
        if arg is not None:
            cmd_with_arg += "=" + str(arg)

        logger.debug(f"executing command to control unit: {cmd_with_arg}")

        def execute_command():
            conn.readbuffer()  # empty buffer
            conn.write(cmd_with_arg)
            time.sleep(0.1)
            buffer = ""
            for i in range(self.BUFFER_READS):
                data = conn.readbuffer()

                if data:
                    buffer += data

                if f"{command}=" in buffer:
                    if "NOT_IMPLEMENTED" in buffer:
                        raise CommandNotImplemented

                    return True, buffer

                time.sleep(self.BUFFER_SLEEP)

            return False, buffer

        with threading.Lock():
            buffer = None

            for i in range(self.COMMAND_RETRY):
                try:
                    success, buffer = execute_command()
                    if success:
                        break
                    time.sleep(self.RETRY_SLEEP)
                except (
                        UnicodeDecodeError, Exception, OSError, pyserial.SerialException,
                        serialutil.SerialException) as e:
                    logger.exception(e)
                    raise pyserial.SerialException

            return True if f"{command}=OK" in buffer else False

    @retry_on_any_exception(retries=EXCEPT_RETRIES)
    def _get_command(self, command):
        conn = self._get_connection()

        logger.debug(f"executing command to control unit: {command}")

        def execute_command():
            conn.readbuffer()  # empty buffer

            conn.write(command)
            time.sleep(0.1)
            buffer = ""

            for i in range(self.BUFFER_READS):
                data = conn.readbuffer()

                if data:
                    buffer += data

                if f"{command}=" not in buffer:
                    time.sleep(self.BUFFER_SLEEP)
                    continue

                return buffer.split(f"{command}=")[1].strip()

        with threading.Lock():
            for i in range(self.COMMAND_RETRY):
                try:
                    data = execute_command()
                    if data: return data
                    time.sleep(self.RETRY_SLEEP)
                except (
                        UnicodeDecodeError, Exception, OSError, pyserial.SerialException,
                        serialutil.SerialException) as e:
                    logger.exception(e)
                    raise pyserial.SerialException

    def _get_connection(self):
        if not self._conn:
            self._conn = ser.Connection(self.com_port, BAUDRATE, timeout=2)
            self._conn.open()
        return self._conn

    def close(self):
        if self._conn: self._conn.close()


if __name__ == "__main__":
    get_online_control_units()
