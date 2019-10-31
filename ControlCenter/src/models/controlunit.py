from src import mvc


class ControlUnitModel(mvc.Model):
    MEMORY_COUNT_THRESHOLD = 1000

    def __init__(self, id):
        self.id = mvc.Observable(self, id)
        self.name = mvc.Observable(self, None)
        self.online = mvc.Observable(self, False)
        self.measurements = mvc.Observable(self, [])

    def set_id(self, id):
        self.id.set(id)

    def get_id(self):
        return self.id.get()

    def set_name(self, name):
        self.name.set(name)

    def get_name(self):
        return self.name.get()

    def set_online(self, boolean):
        self.online.set(boolean)

    def get_online(self):
        return self.online.get()

    def add_measurement(self, measurement):
        measurements = self.measurements.get()
        if len(measurements) > self.MEMORY_COUNT_THRESHOLD:
            measurements.pop(0)
        self.measurements.set(measurements.append(measurement))

    def get_measurements(self):
        return self.measurements
