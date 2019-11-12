import logging
import sqlite3
import threading

import serial as pyserial
import wx

from src import mvc
from src import util
from src.views.settings_view import SettingsView

logger = logging.getLogger(__name__)


class SettingsViewController(mvc.Controller):
    def __init__(self, app, view_parent, controlunit_manager, tabstate_model):
        super().__init__()

        self.app = app
        self.view_parent = view_parent
        self.view = SettingsView(self.view_parent)
        self.controlunit_manager = controlunit_manager
        self.tabstate_model = tabstate_model
        self.tabstate_model.state.add_callback(self.on_tabstate_change)
        self.controlunit_manager.units.add_callback(self.on_controlunits_change)
        self.view.apply_button.Bind(wx.EVT_BUTTON, self.on_apply)
        self.view.delete_button.Bind(wx.EVT_BUTTON, self.on_delete_unit)
        self.selected_unit = None
        self.disable_settings()

        for unit in self.controlunit_manager.get_units():
            unit.model.selected.add_callback(self.on_controlunit_selected_change)
            unit.model.online.add_callback(self.on_controlunit_online_change)

    def on_tabstate_change(self, model, data):
        units = self.controlunit_manager.get_selected_units()
        if len(units) == 1:
            unit = units[0]
            if unit.has_communication():
                self.init_settings_panel(units[0])
            # else:
            #     if self.tabstate_model.is_settings_view():
            #         wx.CallAfter(lambda: self.view.show_error("Device must be connected to apply settings",
            #                                                   title="Device not connected"))

    def on_controlunits_change(self, model, data):
        self.view.delete_button.Disable()
        wx.CallAfter(self.disable_settings)
        for unit in data:
            unit.model.selected.add_callback(self.on_controlunit_selected_change)
            unit.model.online.add_callback(self.on_controlunit_online_change)

    def on_controlunit_online_change(self, model, online):
        wx.CallAfter(self.disable_settings)
        units = self.controlunit_manager.get_selected_units()
        if len(units) == 1:
            unit = units[0]
            if not unit.model.get_selected():
                return
            if online:
                wx.CallAfter(lambda: self.view.delete_button.Disable())
            else:
                wx.CallAfter(lambda: self.view.delete_button.Enable())
            if unit.has_communication():
                self.init_settings_panel(units[0])
            # else:
            #     if self.tabstate_model.is_settings_view():
            #         # wx.CallAfter(lambda: self.view.show_error("Device must be connected to apply settings",
            #         #                                           title="Device not connected"))

    def on_controlunit_selected_change(self, model, data):
        self.view.delete_button.Disable()
        wx.CallAfter(self.disable_settings)
        units = self.controlunit_manager.get_selected_units()
        if len(units) == 1:

            unit = units[0]
            if not unit.model.get_online():
                self.view.delete_button.Enable()

            if unit.has_communication():
                self.init_settings_panel(units[0])
            # else:
            #     if self.tabstate_model.is_settings_view():
                    # wx.CallAfter(lambda: self.view.show_error("Device must be connected to apply settings",
                    #                                           title="Device not connected"))

    def init_settings_panel(self, unit):

        def update_view(window_height, temperature_threshold, light_threshold, color):
            self.view.set_name(unit.model.get_name())
            self.view.set_color(color)
            self.view.set_window_height(window_height if window_height != "ERROR" else "")
            self.view.set_temperature_threshold(temperature_threshold if temperature_threshold != "ERROR" else "")
            self.view.set_light_intensity_threshold(light_threshold if light_threshold != "ERROR" else "")

            """ This code ensures that when a user clicks VERY FAST on two control units at the same time, 
            the application doesnt go into a buggy state. """
            if len(self.controlunit_manager.get_selected_units()) == 1:
                self.enable_settings()
            else:
                self.disable_settings()
                self.view.delete_button.Disable()

            self.view.Update()

        def execute_threaded():
            try:
                window_height = str(unit.comm.get_window_height())
                temperature_threshold = unit.comm.get_temperature_threshold()
                light_threshold = unit.comm.get_light_intensity_threshold()
                color = unit.model.get_color()
                wx.CallAfter(lambda: update_view(window_height, temperature_threshold, light_threshold, color))
            except pyserial.SerialException:
                logger.warning("Serial error")
                # TODO: show user error

        threading.Thread(target=execute_threaded, daemon=True).start()

    def disable_settings(self):
        self.view.disable_inputs()
        self.view.set_name("")
        self.view.set_color(wx.LIGHT_GREY)
        self.view.set_window_height("")
        self.view.set_temperature_threshold("")
        self.view.set_light_intensity_threshold("")

    def enable_settings(self):
        self.view.enable_inputs()

    def validate(self, name, height, color, temperature_threshold, light_intensity_threshold):
        height_ok = False
        temperature_threshold_ok = False
        light_intensity_ok = False

        if util.is_int(height) and 0 < int(height) <= 400:
            height_ok = True
        if util.is_int(temperature_threshold) and -64 < int(temperature_threshold) <= 63:
            temperature_threshold_ok = True
        if util.is_int(light_intensity_threshold) and 0 < int(light_intensity_threshold) <= 100:
            light_intensity_ok = True

        error = ["Failed to apply settings:\n"]
        if not height_ok:
            error.append("- Height must be a value between 0 and 400 in cm.\n")
        if not temperature_threshold_ok:
            error.append("- Temperature threshold must be a value between -64 and 63.\n")
        if not light_intensity_ok:
            error.append("- Temperature threshold must be a value between 0 and 100.\n")

        if not height_ok or not temperature_threshold_ok or not light_intensity_ok:
            return "".join(error)

    def on_apply(self, event):
        name, color, height, temperature_threshold, light_intensity_threshold = self.view.get_settings()

        error = self.validate(name, height, color, temperature_threshold, light_intensity_threshold)

        if error:
            self.view.show_error(error, title="Can not apply settings")
            return

        if not color.IsOk():
            self.view.show_error("Please select a different color", title="Can not apply settings")
            return

        def execute_threaded():
            for unit in self.controlunit_manager.get_selected_units():
                try:
                    device_id = unit.comm.get_id()

                    if device_id:
                        self.update_settings(unit.comm,
                                             unit.model,
                                             device_id,
                                             name,
                                             color,
                                             height,
                                             temperature_threshold,
                                             light_intensity_threshold)
                    else:
                        self.init_device(unit.comm,
                                         unit.model,
                                         unit.model.get_id(),
                                         name,
                                         color,
                                         height,
                                         temperature_threshold,
                                         light_intensity_threshold,
                                         unit.model.get_manual())
                except pyserial.SerialException:
                    logger.warning("Serial error")
                    # TODO: show user error

        threading.Thread(target=execute_threaded, daemon=True).start()

    def init_device(self, comm, model, device_id, name, color, window_height,
                    temperature_threshold, light_intensity_threshold, manual_mode):

        success = comm.initialize(device_id,
                                  window_height,
                                  temperature_threshold,
                                  light_intensity_threshold,
                                  manual_mode)
        if success:
            try:
                model.set_id(model.get_id(), save_db=True)
            except sqlite3.IntegrityError as e:
                unit_id = util.generate_16bit_int()
                device_id = util.encode_controlunit_id(self.app.app_id, unit_id)
                if comm.set_id(device_id):
                    model.set_id(device_id)
                else:
                    wx.CallAfter(lambda: self.view.show_error("Failed to initialize device", title="Failure"))

            model.set_name(name)
            model.set_color(color)
            model.set_initialized(True)
            wx.CallAfter(lambda: self.view.show_success("Successfully initialized device"))
        else:
            wx.CallAfter(lambda: self.view.show_error("Failed to initialize device", title="Failure"))

    def update_settings(self, comm, model, device_id, name, color, window_height,
                        temperature_threshold, light_intensity_threshold):

        if not comm.set_id(device_id):
            wx.CallAfter(lambda: self.view.show_error("Failed to to update id", title="Failure"))
            return
        if not comm.set_window_height(window_height):
            wx.CallAfter(lambda: self.view.show_error("Failed to update window height", title="Failure"))
            return
        if not comm.set_temperature_threshold(temperature_threshold):
            wx.CallAfter(lambda: self.view.show_error("Failed to update temperature threshold", title="Failure"))
            return
        if not comm.set_light_intensity_threshold(light_intensity_threshold):
            wx.CallAfter(lambda: self.view.show_error("Failed to update light intensity threshold", title="Failure"))
            return

        model.set_name(name)
        model.set_color(color)
        wx.CallAfter(lambda: self.view.show_success("Successfully updated device"))

    def on_delete_unit(self, e):
        units = self.controlunit_manager.get_selected_units()

        if len(units) != 1:
            return

        unit = units[0]

        result = wx.MessageBox('Do you want to delete the selected unit?', 'Delete control unit', wx.YES_NO | wx.ICON_EXCLAMATION)

        if result == wx.YES:
            self.controlunit_manager.delete_unit(unit.model.get_id())
