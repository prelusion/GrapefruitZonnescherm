from collections import namedtuple

from src import serialinterface as ser

BAUDRATE = 192500

SensorData = namedtuple("SensorData", ["timestamp",
                                       "temperature",
                                       "shutter_status",
                                       "light_sensitivity"])


def get_online_control_units():
    ports = ser.get_com_ports()

    for port, name in ports:
        print(port, name)
        with ser.connect(port, baudrate=BAUDRATE, timeout=5) as conn:
            print("write data..")
            conn.write("PING")
            print("read data..")
            data = conn.readline()
            print(data)
            print("end")


class Measurement:
    def __init__(self, value, timestamp):
        self.value = value
        self.timestamp = timestamp


class ControlUnitCommunication:
    def __init__(self):
        self.id = None
        self._com_port = None
        self._serial_connection = None

    def is_online(self):
        pass

    def get_shutter_status(self):
        pass

    def get_sensor_data(self):
        pass

    def get_sensor_history(self):
        pass

    def _connect(self):
        pass


class ControlUnitManager:
    def __init__(self):
        self._control_unit_communications = {}
        self._control_unit_models = {}

    def add_control_unit(self, communication, model):
        pass

if __name__ == "__main__":
    get_online_control_units()
