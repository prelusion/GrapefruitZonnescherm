import logging
import threading

import serial as pyserial
import wx

from src import controlunit
from src import mvc
from src.views.manualcontrol_view import ManualControlView

logger = logging.getLogger(__name__)


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
            self.view.toggle_manual_control(model.get_manual())
            if model.get_manual():
                self.view.enable_shutter_control_buttons()
                self.view.toggle_shutter_control(model.get_shutter_status())
        elif units:
            self.view.disable_manual_control()
        else:
            self.view.disable_manual_control()

    def on_manual_control_enable(self):

        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                try:
                    if comm.set_manual(True):
                        wx.CallAfter(lambda: model.set_manual(True))
                        wx.CallAfter(lambda: self.view.enable_shutter_control_buttons())
                        wx.CallAfter(lambda: self.view.manual_toggle.on_toggle_2_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Enable manual control failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Enable manual control failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")
                    # TODO: show user error

        threading.Thread(target=execute, daemon=True).start()

    def on_manual_control_disable(self):
        self.view.disable_shutter_control_buttons()

        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                try:
                    if comm.set_manual(False):
                        wx.CallAfter(lambda: model.set_manual(False))
                        wx.CallAfter(lambda: self.view.manual_toggle.on_toggle_1_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Disable manual control failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Disable manual control failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")
                    # TODO: show user error

        threading.Thread(target=execute, daemon=True).start()

    def on_toggle_up(self):

        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                try:
                    if comm.roll_up():
                        wx.CallAfter(lambda: model.set_shutter_status(model.SHUTTER_GOING_UP))
                        wx.CallAfter(lambda: self.view.shutter_control.on_toggle_1_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Toggle up failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Toggle up failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")
                    # TODO: show user error

        threading.Thread(target=execute, daemon=True).start()

    def on_toggle_down(self):

        def execute():
            for comm, model in self.controlunit_manager.get_selected_units():
                try:
                    if comm.roll_down():
                        wx.CallAfter(lambda: model.set_shutter_status(model.SHUTTER_GOING_DOWN))
                        wx.CallAfter(lambda: self.view.shutter_control.on_toggle_2_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Toggle down failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Toggle down failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")
                    # TODO: show user error

        threading.Thread(target=execute, daemon=True).start()
