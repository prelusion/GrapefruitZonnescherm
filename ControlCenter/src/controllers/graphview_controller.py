from src import mvc
from src.views.graphtab_view import GraphTabView


class GraphViewController(mvc.Controller):
    def __init__(self, view_parent, filter_model, controlunit_manager):
        super().__init__()

        self.filter_model = filter_model
        self.controlunit_manager = controlunit_manager

        # self.graphs_view = src.views.tab_data_view.GraphView(view_parent)
        self.view = GraphTabView(view_parent)

        self.filter_model.filter_connected.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_select_all.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_shutter_up.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_shutter_down.add_callback(self.on_filter_connected_change)

        self.controlunit_manager.units.add_callback(self.on_controlunits_change)

    def on_filter_connected_change(self, model, data):
        pass

    def on_filter_select_all_change(self, model, data):
        pass

    def on_filter_shutter_up_change(self, model, data):
        pass

    def on_filter_shutter_down_change(self, model, data):
        pass

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.measurements.add_callback(self.on_controlunit_measurement_change)
            model.color.add_callback(self.on_controlunit_color_change)
            model.selected.add_callback(self.on_controlunit_selected_change)

    def on_controlunit_measurement_change(self, model, data):
        dates = []
        temps = []
        status = []
        light = []

        for measurement in data:
            dates.append(measurement.timestamp)
            temps.append(measurement.temperature)
            status.append(measurement.shutter_status)
            light.append(measurement.light_intensity)

        # self.temp_view.set_unit(model.get_id(), [dates, temps])
        # self.status_view.set_unit(model.get_id, [dates, status])
        # self.light_view.set_unit(model.get_id, [dates, light])

    def on_controlunit_color_change(self, model, data):
        pass

    def on_controlunit_selected_change(self, model, data):
        print("Model with id:", model.get_id(), "selected:", data)
