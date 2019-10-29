from src import mvc


class ControlUnitModel(mvc.Model):
    MEMORY_COUNT_THRESHOLD = 1000

    def __init__(self, id):
        self._id = mvc.Observable(id)
        self._name = mvc.Observable()
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

    def set_online(self, boolean):
        self._online.set(boolean)

    def get_online(self):
        return self._online.get()

    def add_measurement(self, measurement):
        measurements = self._measurements.get()
        if len(measurements) > self.MEMORY_COUNT_THRESHOLD:
            measurements.pop(0)
        self._measurements.set(measurements.append(measurement))

    def get_measurements(self):
        return self._measurements
