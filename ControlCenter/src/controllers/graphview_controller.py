import wx

from src import mvc
from src.views.tab_data_view import GraphView


class GraphViewController(mvc.Controller):
    def __init__(self, view_parent, filter_model):
        super().__init__()

        self.filter_model = filter_model

        self.view = GraphView(view_parent)

        self.filter_model.filter_connected.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_select_all.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_shutter_up.add_callback(self.on_filter_connected_change)
        self.filter_model.filter_shutter_down.add_callback(self.on_filter_connected_change)

    def on_filter_connected_change(self, prevstate, newstate):
        pass

    def on_filter_select_all_change(self, prevstate, newstate):
        pass

    def on_filter_shutter_up_change(self, prevstate, newstate):
        pass

    def on_filter_shutter_down_change(self, prevstate, newstate):
        pass
