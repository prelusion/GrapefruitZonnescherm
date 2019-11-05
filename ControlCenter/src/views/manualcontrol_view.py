import wx

from src import mvc


class ManualControlView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((0, 50, 50))

