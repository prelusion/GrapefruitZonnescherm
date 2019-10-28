import time
from collections import namedtuple

from src import serialinterface as ser

BAUDRATE = 192500

SensorData = namedtuple("SensorData", ["timestamp",
                                       "temperature",
                                       "shutter_status",
                                       "light_sensitivity"])

Measurement = namedtuple("Measurement", ["timestamp", "value"])


def get_online_control_units():
    """
    Example:

        cu_manager = ControlUnitManager()

        ports = get_online_control_units()

        for port in ports:
            cu_comm = ControlUnitCommunication(port)

            id = cu_comm.get_id()
            if not id:
                cu_comm.set_id(generate_id())

            cu_model = ControlUnitModel(id)

            cu_manager.add_unit(cu_comm, cu_model)

        while True:
            cu_manager.update_models()
            time.sleep(60)
    """
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


class ControlUnitCommunication:
    def __init__(self, port):
        self.id = None
        self._com_port = port
        self._serial_connection = None

    def get_id(self):
        pass

    def is_online(self):
        pass

    def get_shutter_status(self):
        pass

    def get_sensor_data(self):
        return SensorData(time.time(), 5, 5, 5)

    def get_sensor_history(self):
        pass

    def _connect(self):
        pass


class ControlUnitManager:
    def __init__(self):
        self._units = []

    def add_unit(self, communication, model):
        self._units.append((communication, model))

    def get_units(self):
        return self._units

    def update_models(self):
        for comm, model in self._units:
            data = comm.get_sensor_data()
            model.add_temperature(Measurement(data.timestamp, data.temperature))
            model.add_shutter_status(Measurement(data.timestamp, data.shutter_status))
            model.add_light_sensitivity(Measurement(data.timestamp, data.light_sensitivity))


if __name__ == "__main__":
    get_online_control_units()
