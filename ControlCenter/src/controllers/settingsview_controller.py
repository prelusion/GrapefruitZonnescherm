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
    def __init__(self, app, view_parent, controlunit_manager):
        super().__init__()

        self.app = app
        self.view_parent = view_parent
        self.view = SettingsView(self.view_parent)
        self.controlunit_manager = controlunit_manager
        self.controlunit_manager.units.add_callback(self.on_controlunits_change)
        self.view.apply_button.Bind(wx.EVT_BUTTON, self.on_apply)
        self.selected_unit = None
        self.disable_settings()

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.selected.add_callback(self.on_controlunit_selected_change)

    def on_controlunit_selected_change(self, model, data):
        units = self.controlunit_manager.get_selected_units()
        if len(units) > 1:
            self.disable_settings()
        elif len(units) < 1:
            self.disable_settings()
        elif len(units) == 1:
            self.init_settings_panel(units[0])
            self.enable_settings()
        else:
            self.disable_settings()

    def init_settings_panel(self, unit):
        comm, model = unit

        def update_view(window_height, temperature_threshold, light_threshold, color):
            self.view.set_name(model.get_name())
            self.view.set_color(color)
            self.view.set_window_height(window_height)
            self.view.set_temperature_threshold(temperature_threshold)
            self.view.set_light_intensity_threshold(light_threshold)
            self.enable_settings()
            self.view.Update()

        def execute_threaded():
            try:
                window_height = str(comm.get_window_height())
                temperature_threshold = comm.get_temperature_threshold()
                light_threshold = comm.get_light_intensity_threshold()
                color = model.get_color()
                wx.CallAfter(lambda: update_view(window_height, temperature_threshold, light_threshold, color))
            except pyserial.SerialException:
                logger.warning("Serial error")
                # TODO: show user error

        threading.Thread(target=execute_threaded, daemon=True).start()

    def disable_settings(self):
        self.view.disable_inputs()
        self.view.set_name("")
        self.view.set_color("")
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
            for comm, model in self.controlunit_manager.get_selected_units():
                try:
                    device_id = comm.get_id()

                    if device_id:
                        self.update_settings(comm,
                                             model,
                                             device_id,
                                             name,
                                             color,
                                             height,
                                             temperature_threshold,
                                             light_intensity_threshold)
                    else:
                        self.init_device(comm,
                                         model,
                                         model.get_id(),
                                         name,
                                         color,
                                         height,
                                         temperature_threshold,
                                         light_intensity_threshold,
                                         model.get_manual())
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
            model.set_colour(color)
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
        model.set_colour(color)
        wx.CallAfter(lambda: self.view.show_success("Successfully updated device"))
