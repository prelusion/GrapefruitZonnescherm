import wx

from src import mvc
from src import widgets


class FilterView(mvc.View):

    CHECKBOX_CONNECTED = "connected"
    CHECKBOX_STATUS_UP = "status up"
    CHECKBOX_STATUS_DOWN = "status down"
    CHECKBOX_SELECT_ALL = "select all"

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((255, 255, 255))

        # create and set main sizer for filter panel
        main_sizer = wx.GridSizer(2, 1, 0, 0)
        self.SetSizer(main_sizer)

        # create title panel and center title label in it
        title_panel = wx.Panel(self)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_panel.SetSizer(h_sizer)
        label = widgets.CenteredLabel(title_panel, "Filters")
        label.SetFont(wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        h_sizer.Add(label, wx.ID_ANY, wx.EXPAND | wx.ALL )

        # create checkbox panel
        checkbox_panel = wx.Panel(self)
        checkbox_panel.SetBackgroundColour((255, 255, 255))
        gridsizer = wx.GridSizer(2, 2, 5, 5)
        checkboxes = {}
        for checkbox in (self.CHECKBOX_CONNECTED, self.CHECKBOX_STATUS_UP,
                         self.CHECKBOX_SELECT_ALL, self.CHECKBOX_STATUS_DOWN):
            checkboxes[checkbox] = wx.CheckBox(checkbox_panel, label=checkbox)
            gridsizer.Add(checkboxes[checkbox], 0, wx.EXPAND)
        checkbox_panel.SetSizer(gridsizer)

        # add all elements to main sizer
        main_sizer.Add(title_panel,  wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(checkbox_panel,  wx.ID_ANY, wx.EXPAND | wx.ALL)

        # set window border
        self.SetWindowStyle(wx.BORDER_SIMPLE)
