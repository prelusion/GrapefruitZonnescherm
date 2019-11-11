from collections import OrderedDict
from logging import getLogger

import serial as pyserial

from src import db
from src import mvc
from src.models.controlunit import ControlUnitModel

logger = getLogger(__name__)


class ControlUnitManager:
    def __init__(self):
        self.units = mvc.Observable(self, [])  #  (ControlUnitCommunication, ControlUnitModel)
        self.ports = mvc.Observable(self, [])

    def add_unit(self, port, communication, model):
        print("adding unit to manager")
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

    def fetch_units_from_db(self):
        units = []
        for unit in db.select_all(db.TABLE_CONTROL_UNITS):
            db_id, device_id, name, color, created_at = unit
            model = ControlUnitModel(device_id)
            model.set_name(name)
            model.set_color(color)
            model.set_online(False)
            model.set_initialized(True)
            units.append((None, model))

        self.units.set(units)

    def get_units(self):
        """
        :return: [(comm, model), (comm, model)]
        """
        return self.units.get()

    def get_selected_units(self):
        """
        Returns a list of selected control units

        :return: [(comm, model), (comm, model)]
        """
        return [unit for unit in self.units.get() if unit[1].get_selected()]

    def is_port_connected(self, port):
        return port in self.ports.get()

    def get_connected_ports(self):
        return self.ports.get()

    def update_sensor_data(self):
        for comm, model in self.units.get().copy():
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
