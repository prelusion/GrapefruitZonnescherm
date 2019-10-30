import time
from collections import namedtuple, OrderedDict
from concurrent.futures import ThreadPoolExecutor

from src import serialinterface as ser
from src import util
from src.models.controlunit import ControlUnitModel

BAUDRATE = 38400

SensorData = namedtuple("SensorData", ["timestamp",
                                       "temperature",
                                       "shutter_status",
                                       "light_sensitivity"])

Measurement = namedtuple("Measurement", ["timestamp", "value"])


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


class ControlUnitCommunication:
    def __init__(self, port):
        self.id = None
        self.com_port = port
        self._conn = None

    def set_id(self, id):
        pass

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

    def _get_connection(self):
        if not self._conn:
            self._conn = ser.Connection(self.com_port, BAUDRATE, timeout=0.1)
        return self._conn


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

            model.add_temperature(Measurement(data.timestamp, data.temperature))
            model.add_shutter_status(Measurement(data.timestamp, data.shutter_status))
            model.add_light_sensitivity(Measurement(data.timestamp, data.light_sensitivity))


if __name__ == "__main__":
    get_online_control_units()
