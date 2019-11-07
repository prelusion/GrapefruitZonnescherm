from src import mvc
from collections import OrderedDict
from logging import getLogger
import serial as pyserial
logger = getLogger(__name__)


class ControlUnitManager:
    def __init__(self):
        self.units = mvc.Observable(self, OrderedDict())  # "port": <ControlUnitCommunication, ControlUnitModel>

    def add_unit(self, port, communication, model):
        units = self.units.get()
        units[port] = (communication, model)
        self.units.set(units)

    def remove_unit(self, port):
        units = self.units.get()
        if port not in units:
            logger.warning(f"trying to remove unexisting port: {port}")
            return

        comm, model = units[port]
        try:
            comm.close()
        except pyserial.SerialException:
            pass
        del units[port]
        self.units.set(units)

    def get_units(self):
        """
        :return: [(comm, model), (comm, model)]
        """
        return [unit for port, unit in self.units.get().items()]

    def get_selected_units(self):
        """
        Returns a list of selected control units

        :return: [(comm, model), (comm, model)]
        """
        return [unit for port, unit in self.units.get().items() if unit[1].get_selected()]

    def is_port_connected(self, port):
        return port in self.units.get()

    def get_connected_ports(self):
        return list(self.units.get().keys())

    def update_sensor_data(self):
        units = self.units.get().copy()

        for i, port in enumerate(units):
            comm, model = units[port]

            try:
                data = comm.get_sensor_data()

                if data:
                    model.add_measurement(data)
                    model.set_temperature(data.temperature)
                    model.set_shutter_status(data.shutter_status)
                    model.set_light_intensity(data.light_intensity)
            except pyserial.SerialException:
                pass

    def close_connections(self):
        for unit in self.units.get().items():
            comm, model = unit
            try:
                comm.close()
            except pyserial.SerialException:
                pass
