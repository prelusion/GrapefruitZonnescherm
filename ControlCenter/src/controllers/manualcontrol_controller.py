import logging
import threading

import serial as pyserial
import wx

from src import controlunit
from src import mvc
from src.views.manualcontrol_view import ManualControlView

logger = logging.getLogger(__name__)


class ManualControlController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager, tabstate_model):
        super().__init__()

        self.controlunit_manager = controlunit_manager
        self.tabstate_model = tabstate_model
        self.tabstate_model.state.add_callback(self.on_tabstate_change)
        self.view = ManualControlView(view_parent)

        self.view.set_enable_manual_control_callback(self.on_manual_control_enable)
        self.view.set_disable_manual_control_callback(self.on_manual_control_disable)
        self.view.set_toggle_up_callback(self.on_toggle_up)
        self.view.set_toggle_down_callback(self.on_toggle_down)

        if not self.controlunit_manager.get_selected_units():
            self.view.disable_manual_control()

        for unit in self.controlunit_manager.get_units():
            unit.model.selected.add_callback(self.on_unit_selected_change)
            unit.model.name.add_callback(self.on_selected_unit_name_change)
            unit.model.online.add_callback(self.on_unit_online_change)

        self.controlunit_manager.units.add_callback(self.on_units_change)

    def on_unit_online_change(self, model, online):

        def execute():
            self.view.disable_manual_control()

            units = self.controlunit_manager.get_selected_units()

            if len(units) == 1:
                unit = units[0]

                if not online:
                    wx.CallAfter(lambda: self.view.set_selected_unit_name("Selected unit must be online"))
                    return

                if not unit.has_communication() and self.tabstate_model.is_manual_view():
                    self.view.set_selected_unit_name("Selected unit must be online")
                    return

                self.view.enable_manual_control()
                self.view.toggle_manual_control(model.get_manual())
                self.view.set_selected_unit_name(model.get_name())
                if model.get_manual():
                    self.view.enable_shutter_control_buttons()
                    self.view.toggle_shutter_control(model.get_shutter_status())
            elif units:
                self.view.set_selected_unit_name("Please select one unit")
                self.view.disable_manual_control()
            else:
                self.view.set_selected_unit_name()
                self.view.disable_manual_control()

        wx.CallAfter(execute)

    def on_tabstate_change(self, model, data):
        if self.tabstate_model.is_manual_view():
            units = self.controlunit_manager.get_selected_units()
            if len(units) == 1:

                unit = units[0]

                if not unit.has_communication() and self.tabstate_model.is_manual_view():
                    self.view.disable_manual_control()
                    return

    def on_units_change(self, model, data):
        for unit in self.controlunit_manager.get_units():
            unit.model.selected.add_callback(self.on_unit_selected_change)
            unit.model.name.add_callback(self.on_selected_unit_name_change)
            unit.model.online.add_callback(self.on_unit_online_change)

    def on_unit_selected_change(self, model, data):
        self.view.disable_manual_control()
        units = self.controlunit_manager.get_selected_units()

        if len(units) == 1:
            unit = units[0]

            if not unit.has_communication() and self.tabstate_model.is_manual_view():
                self.view.set_selected_unit_name("Selected unit must be online")
                return

            self.view.enable_manual_control()
            self.view.toggle_manual_control(model.get_manual())
            self.view.set_selected_unit_name(model.get_name())

            if model.get_manual():
                self.view.enable_shutter_control_buttons()
                self.view.toggle_shutter_control(model.get_shutter_status())

        elif units:
            self.view.set_selected_unit_name("Please select one unit")
            self.view.disable_manual_control()
        else:
            self.view.set_selected_unit_name()
            self.view.disable_manual_control()

    def on_selected_unit_name_change(self, mode, data):
        units = self.controlunit_manager.get_selected_units()
        if len(units) == 1:
            unit = units[0]
            self.view.set_selected_unit_name(unit.model.get_name())

    def on_manual_control_enable(self):

        def execute():
            for unit in self.controlunit_manager.get_selected_units():
                try:
                    if unit.comm.set_manual(True):
                        wx.CallAfter(lambda: unit.model.set_manual(True))
                        wx.CallAfter(lambda: self.view.enable_shutter_control_buttons())
                        wx.CallAfter(lambda: self.view.manual_toggle.on_toggle_2_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Enable manual control failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Enable manual control failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")

        threading.Thread(target=execute, daemon=True).start()

    def on_manual_control_disable(self):
        self.view.disable_shutter_control_buttons()

        def execute():
            for unit in self.controlunit_manager.get_selected_units():
                try:
                    if unit.comm.set_manual(False):
                        wx.CallAfter(lambda: unit.model.set_manual(False))
                        wx.CallAfter(lambda: self.view.manual_toggle.on_toggle_1_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Disable manual control failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Disable manual control failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")

        threading.Thread(target=execute, daemon=True).start()

    def on_toggle_up(self):

        def execute():
            for unit in self.controlunit_manager.get_selected_units():
                try:
                    if unit.comm.roll_up():
                        wx.CallAfter(lambda: unit.model.set_shutter_status(unit.model.SHUTTER_GOING_UP))
                        wx.CallAfter(lambda: self.view.shutter_control.on_toggle_1_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Toggle up failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Toggle up failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")

        threading.Thread(target=execute, daemon=True).start()

    def on_toggle_down(self):

        def execute():
            for unit in self.controlunit_manager.get_selected_units():
                try:
                    if unit.comm.roll_down():
                        wx.CallAfter(lambda: unit.model.set_shutter_status(unit.model.SHUTTER_GOING_DOWN))
                        wx.CallAfter(lambda: self.view.shutter_control.on_toggle_2_success())
                    else:
                        wx.CallAfter(lambda: self.view.show_error("Toggle down failure"))
                except controlunit.CommandNotImplemented:
                    wx.CallAfter(lambda: self.view.show_error(
                        "Toggle down failure: functionality was not implemented on this control unit"))
                except pyserial.SerialException:
                    logger.warning("Serial error")

        threading.Thread(target=execute, daemon=True).start()
