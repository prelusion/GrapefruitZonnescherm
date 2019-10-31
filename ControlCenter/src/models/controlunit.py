from src import mvc


class ControlUnitModel(mvc.Model):
    MEMORY_COUNT_THRESHOLD = 1000

    def __init__(self, id):
        self._id = mvc.Observable(id)
        self._name = mvc.Observable()
        self._colour = mvc.Observable("#fc03df")
        self._online = mvc.Observable(False)
        self._measurements = mvc.Observable([])

    def set_id(self, id):
        self._id.set(id)

    def get_id(self):
        return self._id.get()

    def set_name(self, name):
        self._name.set(name)

    def get_name(self):
        return self._name.get()

    def set_colour(self, colour):
        self._colour.set(colour)

    def get_colour(self):
        return self._colour.get()

    def set_online(self, boolean):
        self._online.set(boolean)

    def get_online(self):
        return self._online.get()

    def add_measurement(self, measurement):
        measurements = self._measurements.get()
        if len(measurements) > self.MEMORY_COUNT_THRESHOLD:
            measurements.pop(0)
        measurements.append(measurement)
        self._measurements.set(measurements)

    def get_measurements(self, interval=60, limit=1000):
        return self._measurements
