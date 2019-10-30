from src import mvc
from collections import OrderedDict


class ControlUnitManager:
    def __init__(self):
        self.units = mvc.Observable(OrderedDict())  # "port": <communication, model>

    def add_unit(self, port, communication, model):
        units = self.units.get()
        units[port] = (communication, model)
        self.units.set(units)

    def remove_unit(self, port):
        print("removing unit with port from manager:", port)
        units = self.units.get()
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
