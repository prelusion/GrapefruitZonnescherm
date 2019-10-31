from src import mvc
from collections import OrderedDict
from logging import getLogger

logger = getLogger(__name__)


class ControlUnitManager:
    def __init__(self):
        self.units = mvc.Observable(self, OrderedDict())  # "port": <ControlUnitCommunication, ControlUnitModel>

    def add_unit(self, port, communication, model):
        print("CU Manager add:", port)
        units = self.units.get()
        units[port] = (communication, model)
        self.units.set(units)

    def remove_unit(self, port):
        print("CU Manager remove:", port)
        units = self.units.get()
        if port not in units:
            logger.warning(f"trying to remove unexisting port: {port}")
            return

        comm, model = units[port]
        comm.close()
        del units[port]
        self.units.set(units)

    def get_units(self):
        return self.units.get()

    def is_port_connected(self, port):
        return port in self.units.get()

    def get_connected_ports(self):
        return list(self.units.get().keys())

    def update_models(self):
        for i, unit in enumerate(self.units.get().copy()):
            comm, model = unit

            data = comm.get_sensor_data()

            if not data:
                del self.units[i]

            model.add_measurement(data)

    def close_connections(self):
        for unit in self.units.get().items():
            comm, model = unit
            comm.close()
