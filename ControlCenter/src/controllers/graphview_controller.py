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

    def redraw_all_units(self):
        units = self.controlunit_manager.get_selected_units()

        for unit in units:
            comm, model = unit
            self.update_graph(model, model.get_measurements())

    def on_controlunit_selected_change(self, model, selected):
        if selected:
            model.measurements.add_callback(self.on_controlunit_measurement_change)
            model.color.add_callback(self.on_controlunit_color_change)
        else:
            model.measurements.del_callback(self.on_controlunit_measurement_change)
            model.color.del_callback(self.on_controlunit_color_change)
            self.view.remove_device(model.get_id())
            self.redraw_all_units()

    def on_controlunit_measurement_change(self, model, data):
        self.update_graph(model, data)

    def on_controlunit_color_change(self, model, data):
        pass

    def update_graph(self, model, data=None):
        if not data:
            data = model.get_measurements()

        measurements = copy.deepcopy(
            data)  # copy otherwise we get RuntimeError if new measurements are added during iteration
        timestamps = list(map(lambda x: x.timestamp, measurements))
        temperatures = list(map(lambda x: x.temperature, measurements))
        shutter_status = list(map(lambda x: x.shutter_status, measurements))
        light_intensity = list(map(lambda x: x.light_intensity, measurements))

        self.view.update_temperature_graph(model.get_id(),
                                           model.get_color(),
                                           timestamps,
                                           temperatures)

        self.view.update_status_graph(model.get_id(),
                                      model.get_color(),
                                      timestamps,
                                      shutter_status)

        self.view.update_light_graph(model.get_id(),
                                     model.get_color(),
                                     timestamps,
                                     light_intensity)
