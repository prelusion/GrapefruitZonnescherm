from src import mvc
from src import controlunit


class ControlUnitModel(mvc.Model):

    MEMORY_COUNT_THRESHOLD = 1000

    def __init__(self):
        self._id = mvc.Observable()
        self._name = mvc.Observable()
        self._online = mvc.Observable(False)
        self._temperatures = mvc.Observable([])
        self._shutter_status = mvc.Observable([])
        self._light_sensitivities = mvc.Observable([])

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

    def add_temperature(self, temperature: controlunit.Measurement):
        temperatures = self._temperatures.get()
        if len(temperatures) > self.MEMORY_COUNT_THRESHOLD:
            temperatures.pop(0)
        self._temperatures.set(temperatures.append(temperature))

    def get_current_temperature(self):
        temperatures = self._temperatures.get()
        return temperatures and  temperatures[-1]

    def get_temperatures(self):
        return self._temperatures.get()

    def add_shutter_status(self, status: controlunit.Measurement):
        shutter_status = self._shutter_status.get()
        if len(shutter_status) > self.MEMORY_COUNT_THRESHOLD:
            shutter_status.pop(0)
        self._shutter_status.set(shutter_status.append(status))

    def get_current_shutter_status(self):
        shutter_status = self._shutter_status.get()
        return shutter_status and shutter_status[-1]

    def get_shutter_status(self):
        return self._shutter_status.get()

    def add_light_sensitivity(self, light_sensitivity: controlunit.Measurement):
        light_sensitivities = self._light_sensitivities.get()
        if len(light_sensitivities) > self.MEMORY_COUNT_THRESHOLD:
            light_sensitivities.pop(0)
        self._shutter_status.set(light_sensitivities.append(light_sensitivity))

    def get_current_light_sensitivity(self):
        light_sensitivities = self._light_sensitivities.get()
        return light_sensitivities and light_sensitivities[-1]

    def get_light_sensitivities(self):
        return self._light_sensitivities.get()
