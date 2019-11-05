from src import mvc
from src.views.settings_view import SettingsView


class SettingsViewController(mvc.Controller):
    def __init__(self, view_parent):
        super().__init__()

        self.view = SettingsView(view_parent)

        #TEST DATA
        self.view.SetName("Test unit")
        self.view.SetHeight("200")
        self.view.SetColor("#FF0000")


