import wx
import threading
from src import mvc
from src.views.settings_view import SettingsView


class SettingsViewController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

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
        else:
            self.disable_settings()

    def init_settings_panel(self, unit):
        comm, model = unit

        def update_view(window_height, temperature_threshold, light_threshold):
            self.view.set_name(model.get_name())
            self.view.set_color("TEST")
            self.view.set_window_height(window_height)
            self.view.set_temperature_threshold(temperature_threshold)
            self.view.set_light_intensity_threshold(light_threshold)
            self.enable_settings()
            self.view.Update()

        def execute_threaded():
            window_height = str(comm.get_window_height())
            temperature_threshold = comm.get_temperature_threshold()
            light_threshold = comm.get_light_intensity_threshold()
            wx.CallAfter(lambda: update_view(window_height, temperature_threshold, light_threshold))

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

    def on_apply(self, event):

        settings = {
            # "name":(self.view.get_name(), lambda x, value: comm.set_name(value)),
            "height": (self.view.get_window_height(), lambda x, value: comm.set_window_height(value)),
            # "color": self.view.get_color(),
            "max_temp": (self.view.get_temperature_threshold(), lambda x, value: comm.set_temperature_threshold(value)),
            "max_light": (
                self.view.get_light_intensity_threshold(), lambda x, value: comm.set_light_intensity_threshold(value))
        }

        all_errors = []
        for comm, model in self.controlunit_manager.get_selected_units():
            errors = []

            for name, setter in settings.items():
                value, function = setter
                if function(comm, value):
                    function(model, value)
                else:
                    errors.append("Error setting " + name)

            all_errors.append((model.get_id(), errors))
