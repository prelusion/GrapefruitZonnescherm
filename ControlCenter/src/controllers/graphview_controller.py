import copy

from src import mvc
from src.views.graphtab_view import GraphTabView


class GraphViewController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.controlunit_manager = controlunit_manager

        self.view = GraphTabView(view_parent)

        self.controlunit_manager.units.add_callback(self.on_controlunits_change)
        self.units = []

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.selected.add_callback(self.on_controlunit_selected_change)

    def on_controlunit_selected_change(self, model, selected):
        if selected:
            model.measurements.add_callback(self.on_controlunit_measurement_change)
            model.color.add_callback(self.on_controlunit_color_change)
        else:
            model.measurements.del_callback(self.on_controlunit_measurement_change)
            model.color.del_callback(self.on_controlunit_color_change)
            self.view.clear_trace(model.get_id())

    def on_controlunit_measurement_change(self, model, data):
        data = copy.deepcopy(data)  # copy otherwise we get RuntimeError if new measurements are added during iteration

        timestamps = list(map(lambda x: x.timestamp, data))
        temperatures = list(map(lambda x: x.temperature, data))
        shutter_status = list(map(lambda x: x.shutter_status, data))
        light_intensity = list(map(lambda x: x.light_intensity, data))

        self.view.update_temperature_graph(model.get_id(),
                                           model.get_name(),
                                           model.get_color(),
                                           timestamps,
                                           temperatures)

    def on_controlunit_color_change(self, model, data):
        pass


# [Measurement(), Measurment()]
# [100, 123, 99, 32]


