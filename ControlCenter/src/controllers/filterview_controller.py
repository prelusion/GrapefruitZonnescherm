import wx

from src import mvc
from src.views.filter_view import FilterView


class FilterViewController(mvc.Controller):
    def __init__(self, view_parent, filter_model):
        super().__init__()

        self.filter_model = filter_model

        self.view = FilterView(view_parent)

        self.view.Bind(wx.EVT_CHECKBOX,self.on_checkbox_change)

    def on_checkbox_change(self, event):
        e = event.GetEventObject()
        label = e.GetLabel()
        value = e.GetValue()

        distributor = {
            self.view.CHECKBOX_CONNECTED: lambda value: self.on_checkbox_connected(value),
            self.view.CHECKBOX_SELECT_ALL: lambda value: self.on_checkbox_select_all(value),
            self.view.CHECKBOX_STATUS_UP: lambda value: self.on_checkbox_status_up(value),
            self.view.CHECKBOX_STATUS_DOWN: lambda value: self.on_checkbox_status_down(value)
        }

        distributor[label](value)

    def on_checkbox_connected(self, value):
        self.filter_model.set_filter_connected(bool(value))

    def on_checkbox_select_all(self, value):
        self.filter_model.set_filter_select_all(bool(value))

    def on_checkbox_status_up(self, value):
        self.filter_model.set_filter_shutter_up(bool(value))

    def on_checkbox_status_down(self, value):
        self.filter_model.set_filter_shutter_down(bool(value))
