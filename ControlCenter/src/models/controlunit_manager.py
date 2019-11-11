from collections import OrderedDict
from logging import getLogger

import serial as pyserial

from src import db
from src import mvc
from src.models.controlunit import ControlUnitModel

logger = getLogger(__name__)


class Unit:
    def __init__(self, model):
        self.model = model
        self.comm = None

    def set_communication(self, comm):
        self.comm = comm
        self.model.set_online(True)

    def has_communication(self):
        return self.comm is not None

    def remove_communication(self):
        try:
            self.comm.close()
        except pyserial.SerialException:
            pass
        self.comm = None
        self.model.set_online(False)


class ControlUnitManager:
    def __init__(self):
        self.units = mvc.Observable(self, [])  # [Unit)

    def get_unit(self, device_id):
        units = [unit for unit in self.units.get() if unit.model.get_id() == device_id]
        if len(units) == 1: return units[0]

    def add_communication(self, device_id, comm):
        self.get_unit(device_id).set_communication(comm)

    def remove_communication(self, port):
        for unit in self.units.get():
            if unit.has_communication() and unit.comm.port == port:
                unit.remove_communication()
                return
        else:
            logger.warning(f"trying to remove connection from unexisting port: {port}")

    def add_unit(self, device_id, communication, port):
        print("adding unit to manager")
        # units = self.units.get()
        # units[port] = (communication, model)
        # self.units.set(units)

    def remove_unit(self, port):
        units = self.units.get().copy()

        for i, unit in enumerate(units):
            if unit.has_communication() and unit.comm.port == port:
                try:
                    unit.comm.close()
                except pyserial.SerialException:
                    pass

                del units[i]
                self.units.set(units)
                return
        else:
            logger.warning(f"trying to remove unexisting port: {port}")

    def fetch_units_from_db(self):
        units = []
        for unit in db.select_all(db.TABLE_CONTROL_UNITS):
            db_id, device_id, name, color, created_at = unit
            model = ControlUnitModel(device_id)
            model.set_name(name)
            model.set_color(color)
            model.set_online(False)
            model.set_initialized(True)
            units.append(Unit(model))

        self.units.set(units)

    def get_units(self):
        """
        :return: [(comm, model), (comm, model)]
        """
        print("get units", self.units.get())
        return self.units.get()

    def get_selected_units(self):
        """
        Returns a list of selected control units

        :return: [(comm, model), (comm, model)]
        """
        return [unit for unit in self.units.get() if unit.model.get_selected()]

    def is_port_connected(self, port):
        return port in self.get_connected_ports()

    def get_connected_ports(self):
        return [unit.comm.port for unit in self.units.get() if unit.comm]

    def update_sensor_data(self):
        print("update sensor data")
        for unit in self.units.get().copy():
            print(unit)
            print(unit.has_communication())
            if not unit.has_communication():
                continue
            try:
                data = unit.comm.get_sensor_data()

                if data:
                    unit.model.add_measurement(data)
                    unit.model.set_temperature(data.temperature)
                    unit.model.set_shutter_status(data.shutter_status)
                    unit.model.set_light_intensity(data.light_intensity)
            except pyserial.SerialException:
                pass

    def close_connections(self):
        for unit in self.units.get():
            try:
                unit.comm.close()
            except pyserial.SerialException:
                pass
