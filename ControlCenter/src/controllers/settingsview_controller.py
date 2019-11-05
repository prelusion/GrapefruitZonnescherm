import wx

from src import mvc
from src.views.settings_view import SettingsView


class SettingsViewController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.view = SettingsView(view_parent)

        self.controlunit_manager = controlunit_manager
        #TEST DATA
        self.view.set_name("Test unit")
        self.view.set_height("200")
        self.view.set_color("#FF0000")
        self.controlunit_manager.units.add_callback(self.on_controlunits_change)
        self.view.apply_button.Bind(wx.EVT_BUTTON, self.on_apply)

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.selected.add_callback(self.on_controlunit_selected_change)

    def on_controlunit_selected_change(self, model, data):
        pass

    def on_apply(self):

        settings= {
        "name":(self.view.get_name(), lambda x, value: comm.set_name(value)),
        "height":self.view.get_height(),
        "color": self.view.get_color(),
        "max_temp": self.view.get_max_temp(),
        "max_light": self.view.get_max_light()
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



