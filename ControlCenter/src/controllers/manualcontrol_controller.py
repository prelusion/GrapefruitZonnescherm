import threading

import wx

from src import mvc
from src.views.manualcontrol_view import ManualControlView


def execute_threaded(fn, callback):
    if fn():
        wx.CallAfter(callback)


class ManualControlController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.controlunit_manager = controlunit_manager

        self.view = ManualControlView(view_parent)

        self.view.set_enable_manual_control_callback(self.on_manual_control_enable)
        self.view.set_disable_manual_control_callback(self.on_manual_control_disable)
        self.view.set_toggle_up_callback(self.on_toggle_up)
        self.view.set_toggle_down_callback(self.on_toggle_down)

        if not self.controlunit_manager.get_selected_units():
            self.view.disable_manual_control()

        self.controlunit_manager.units.add_callback(self.on_units_change)

    def on_units_change(self, model, data):
        for comm, model in self.controlunit_manager.get_units():
            model.selected.add_callback(self.on_unit_selected_change)

    def on_unit_selected_change(self, model, data):
        units = self.controlunit_manager.get_selected_units()
        if len(units) == 1:
            comm, model = units[0]
            self.view.enable_manual_control()
            self.view.set_manual_enabled(model.get_manual())
        elif units:
            self.view.enable_manual_control()
            self.view.set_manual_enabled(True)
        else:
            self.view.disable_manual_control()

    def on_manual_control_enable(self):
        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                if comm.set_manual(True):
                    wx.CallAfter(lambda: model.set_manual(True))

        threading.Thread(target=execute).start()

    def on_manual_control_disable(self):

        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                if comm.set_manual(False):
                    wx.CallAfter(lambda: model.set_manual(False))

        threading.Thread(target=execute).start()

    def on_toggle_up(self):

        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                if comm.roll_up():
                    wx.CallAfter(lambda: model.set_shutter_status(model.SHUTTER_GOING_UP))

        threading.Thread(target=execute).start()

    def on_toggle_down(self):

        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                if comm.roll_down():
                    wx.CallAfter(lambda: model.set_shutter_status(model.SHUTTER_GOING_DOWN))

        threading.Thread(target=execute).start()
