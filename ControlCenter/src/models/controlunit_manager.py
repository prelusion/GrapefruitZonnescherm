from src import mvc


class ControlUnitManager:
    def __init__(self):
        self.units = mvc.Observable([])

    def add_unit(self, communication, model):
        self.units.set(self.units.get().append((communication, model)))

    def get_units(self):
        return self.units.get()

    # def update_models(self):
    #     for i, unit in enumerate(self._units.copy())/:
    #         comm, model = unit
    #
    #         data = comm.get_sensor_data()
    #
    #         if not data:
    #             del self._units[i]
    #
    #         model.add_temperature(Measurement(data.timestamp, data.temperature))
    #         model.add_shutter_status(Measurement(data.timestamp, data.shutter_status))
    #         model.add_light_sensitivity(Measurement(data.timestamp, data.light_sensitivity))
    #