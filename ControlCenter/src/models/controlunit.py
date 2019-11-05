from src import mvc


class ControlUnitModel(mvc.Model):
    MEMORY_COUNT_THRESHOLD = 200

    def __init__(self, id):
        self.id = mvc.Observable(self, id)
        self.name = mvc.Observable(self, "unnamed")
        self.online = mvc.Observable(self, False)
        self.mode = mvc.Observable(self, "auto")
        self.color = mvc.Observable(self, None)
        self.measurements = mvc.Observable(self, [])
        self.shutter_status = mvc.Observable(self, None)
        self.temperature = mvc.Observable(self, 0)
        self.light_intensity = mvc.Observable(self, 0)
        self.selected = mvc.Observable(self, False)

    def set_id(self, id):
        self.id.set(id)

    def get_id(self):
        return self.id.get()

    def set_name(self, name):
        self.name.set(name)

    def get_name(self):
        return self.name.get()

    def set_colour(self, colour):
        self.color.set(colour)

    def get_colour(self):
        return self.color.get()

    def set_online(self, boolean):
        self.online.set(boolean)

    def get_online(self):
        return self.online.get()

    def set_mode(self, boolean):
        self.mode.set(boolean)

    def get_mode(self):
        return self.mode.get()

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

    def get_measurements(self):
        return self.measurements

    def set_selected(self, value):
        self.selected.set(value)

    def get_selected(self):
        return self.selected.get()
