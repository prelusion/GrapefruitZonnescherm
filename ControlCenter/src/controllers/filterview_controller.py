import wx

from src import mvc
from src.views.filter_view import FilterView


class FilterViewController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.controlunit_manager = controlunit_manager

        self.view = FilterView(view_parent)

        self.view.Bind(wx.EVT_CHECKBOX, self.on_checkbox_change)

        self.filters = {
            self.view.CHECKBOX_CONNECTED: False,
            self.view.CHECKBOX_SELECT_ALL: False,
            self.view.CHECKBOX_STATUS_UP: False,
            self.view.CHECKBOX_STATUS_DOWN: False,
        }

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

    def _reset(self):
        for unit in self.controlunit_manager.get_units():
            unit.model.set_selected(False)

    def _select(self):
        self._reset()

        for unit in self.controlunit_manager.get_units():
            if self.filters[self.view.CHECKBOX_CONNECTED]:
                if unit.model.get_online(): unit.model.set_selected(True)
            if self.filters[self.view.CHECKBOX_STATUS_UP]:
                if unit.model.get_shutter_status() == unit.model.SHUTTER_UP: unit.model.set_selected(True)
            if self.filters[self.view.CHECKBOX_STATUS_DOWN]:
                if unit.model.get_shutter_status() == unit.model.SHUTTER_DOWN: unit.model.set_selected(True)
            if self.filters[self.view.CHECKBOX_SELECT_ALL]:
                unit.model.set_selected(True)

    def on_checkbox_connected(self, boolean):
        self.filters[self.view.CHECKBOX_CONNECTED] = boolean
        self._select()

    def on_checkbox_select_all(self, boolean):
        self.filters[self.view.CHECKBOX_SELECT_ALL] = boolean
        self._select()

    def on_checkbox_status_up(self, boolean):
        self.filters[self.view.CHECKBOX_STATUS_UP] = boolean
        self._select()

    def on_checkbox_status_down(self, boolean):
        self.filters[self.view.CHECKBOX_STATUS_DOWN] = boolean
        self._select()
