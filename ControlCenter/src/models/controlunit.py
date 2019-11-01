from src import mvc


class ControlUnitModel(mvc.Model):
    MEMORY_COUNT_THRESHOLD = 1000

    def __init__(self, id):
        self.id = mvc.Observable(self, id)
        self.name = mvc.Observable(self, "unnamed")
        self.online = mvc.Observable(self, False)
        self.mode = mvc.Observable(self, "auto")
        self.color = mvc.Observable(self, None)
        self.measurements = mvc.Observable(self, [])
        self.shutter_status = mvc.Observable(self, "up")

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

    def add_measurement(self, measurement):
        measurements = self.measurements.get()
        if len(measurements) > self.MEMORY_COUNT_THRESHOLD:
            measurements.pop(0)
        self.measurements.set(measurements.append(measurement))

    def get_measurements(self):
        return self.measurements

    def get_current_temperature(self):
        return "23.5"
