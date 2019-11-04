import wx

from src import mvc


class FilterView(mvc.View):

    CHECKBOX_CONNECTED = "connected"
    CHECKBOX_STATUS_UP = "status up"
    CHECKBOX_STATUS_DOWN = "status down"
    CHECKBOX_SELECT_ALL = "select all"

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((255, 255, 255))

        self.gridsizer = wx.GridSizer(2, 2, 5, 5)
        self.SetWindowStyle(wx.BORDER_SIMPLE)

        self.checkboxes = {}

        for checkbox in (self.CHECKBOX_CONNECTED, self.CHECKBOX_STATUS_UP,
                         self.CHECKBOX_SELECT_ALL, self.CHECKBOX_STATUS_DOWN):

            self.checkboxes[checkbox] = wx.CheckBox(self, label=checkbox)
            self.gridsizer.Add(self.checkboxes[checkbox], 0, wx.EXPAND)

        self.SetSizer(self.gridsizer)
