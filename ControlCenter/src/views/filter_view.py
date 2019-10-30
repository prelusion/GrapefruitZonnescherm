import wx

from src import mvc


class FilterView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((255, 255, 255))

        self.gridsizer = wx.GridSizer(2, 2, 5, 5)

        self.checkboxes = {}
        for checkbox in ("connected", "status up", "select all", "status down"):
            self.checkboxes[checkbox] = wx.CheckBox(self, label=checkbox)
            self.gridsizer.Add(self.checkboxes[checkbox], 0, wx.EXPAND)

        self.SetSizer(self.gridsizer)
