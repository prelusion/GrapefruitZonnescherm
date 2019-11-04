from src import mvc


class SettingsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((100, 255, 100))
