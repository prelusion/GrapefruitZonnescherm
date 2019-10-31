import wx

from src import mvc
from src.views.tab_data_view import GraphView


class GraphViewController(mvc.Controller):
    def __init__(self, view_parent, filter_model, controlunit_manager):
        super().__init__()

        self.filter_model = filter_model
        self.controlunit_manager = controlunit_manager

        self.view = GraphView(view_parent)

        self.filter_model.filter_connected.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_select_all.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_shutter_up.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_shutter_down.add_callback(self.on_filter_connected_change)

        # self.controlunit_manager.units.add_callback(self.on_controlunits_change)

    def on_filter_connected_change(self, model, data):
        pass

    def on_filter_select_all_change(self, model, data):
        pass

    def on_filter_shutter_up_change(self, model, data):
        pass

    def on_filter_shutter_down_change(self, model, data):
        pass

    # def on_controlunits_change(self, manager_model, prevstate, newstate):
    #     for port in newstate.keys():
    #         comm, unit_model = newstate[port]
    #         unit_model.measurements.add_callback(self.on_controlunit_measurement_change)
    #
    # def on_controlunit_measurement_change(self, model, prevstate, newstate):
    #     unit_id = model.get_id()
    #     measurements = newstate
