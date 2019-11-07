import wx
from src.measurement import Measurement

from src import db
from src import mvc
from src import util


class ControlUnitModel(mvc.Model):
    MEMORY_COUNT_THRESHOLD = 200
    SHUTTER_UP = 0
    SHUTTER_DOWN = 1
    SHUTTER_GOING_UP = 2
    SHUTTER_GOING_DOWN = 3

    def __init__(self, id):
        self.initialized = mvc.Observable(self, False)
        self.id = mvc.Observable(self, id)
        self.name = mvc.Observable(self, "uninitialized")
        self.online = mvc.Observable(self, True)
        self.manual = mvc.Observable(self, False)
        self.color = mvc.Observable(self, wx.NullColour)
        self.measurements = mvc.Observable(self, [])
        self.shutter_status = mvc.Observable(self, None)
        self.temperature = mvc.Observable(self, 0)
        self.light_intensity = mvc.Observable(self, 0)
        self.selected = mvc.Observable(self, False)

    def set_initialized(self, boolean):
        self.initialized = boolean

    def get_initialized(self):
        return self.initialized

    def set_id(self, id, save_db=False):
        """ ID is not automatically saved to database because we only
        want to save it when the device has been configured / initialized. """
        self.id.set(id)

        if save_db:
            db.insert(db.TABLE_CONTROL_UNITS, "(device_id)", f"('{id}')")

    def get_id(self):
        return self.id.get()

    def set_name(self, name):
        if not name:
            name = "uninitialized"
        self.name.set(name)
        db.update(db.TABLE_CONTROL_UNITS, f"name = '{name}'", f"device_id = {self.get_id()}")

    def get_name(self):
        name = db.select_columns(db.TABLE_CONTROL_UNITS, "name", f"device_id = {self.get_id()}")
        if name and len(name) == 1:
            self.set_name(name[0][0])
        return self.name.get()

    def set_colour(self, colour):
        self.color.set(colour)
        db.update(db.TABLE_CONTROL_UNITS, f"color = '{colour}'", f"device_id = {self.get_id()}")

    def get_colour(self):
        color = db.select_columns(db.TABLE_CONTROL_UNITS, "color", f"device_id = {self.get_id()}")
        if color and len(color) == 1:
            color = color[0][0]
            if color:
                self.color.set(util.deserialize_color(color))
        return self.color.get()

    def set_online(self, boolean):
        self.online.set(boolean)

    def get_online(self):
        return self.online.get()

    def set_manual(self, boolean):
        self.manual.set(bool(boolean))

    def get_manual(self):
        return self.manual.get()

    def set_shutter_status(self, value):
        self.shutter_status.set(value)

    def get_shutter_status(self):
        return self.shutter_status.get()

    def set_temperature(self, value):
        self.temperature.set(value)

    def get_temperature(self):
        return self.temperature.get()

    def set_light_intensity(self, value):
        return self.light_intensity.set(value)

    def get_light_intensity(self):
        return self.light_intensity.get()

    def add_measurement(self, measurement):
        measurements = self.measurements.get()
        if len(measurements) > self.MEMORY_COUNT_THRESHOLD:
            measurements.pop(0)
        measurements.append(measurement)
        self.measurements.set(measurements)

        db.insert(db.TABLE_MEASUREMENTS,
                  "(device_id, temperature, light_intensity, shutter_status, from_history, timestamp)",
                  f"({self.get_id()}, {measurement.temperature}, {measurement.light_intensity}, {measurement.shutter_status}, 0, {measurement.timestamp})")

    def get_measurements(self):
        # return self.measurements
        measurements = db.select_columns(db.TABLE_MEASUREMENTS,
                                         "temperature, light_intensity, shutter_status, timestamp",
                                         f"device_id = {self.get_id()}",
                                         orderby="timestamp ASC",
                                         size=self.MEMORY_COUNT_THRESHOLD)

        converted = []
        for measurement in measurements:
            temperature, light_intensity, shutter_status, timestamp = measurement
            converted.append(Measurement(timestamp, temperature, shutter_status, light_intensity))

        self.measurements.set(converted)

        return converted

    def set_selected(self, value):
        self.selected.set(value)

    def get_selected(self):
        return self.selected.get()
