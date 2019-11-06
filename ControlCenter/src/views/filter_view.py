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
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label.SetFont(font)
        h_sizer.Add(label, wx.ID_ANY, wx.EXPAND | wx.ALL )

        # Create lower panel and its sizers
        lower_panel = wx.Panel(self)
        checkbox_sizer = wx.BoxSizer()
        checkbox_sizer.AddStretchSpacer(1)


        # create checkbox panel
        checkbox_panel = wx.Panel(lower_panel)
        checkbox_panel.SetBackgroundColour((255, 255, 255))
        gridsizer = wx.GridSizer(2, 2, 5, 5)
        checkboxes = {}
        for checkbox in (self.CHECKBOX_CONNECTED, self.CHECKBOX_STATUS_UP,
                         self.CHECKBOX_SELECT_ALL, self.CHECKBOX_STATUS_DOWN):
            checkboxes[checkbox] = wx.CheckBox(checkbox_panel, label=checkbox)
            gridsizer.Add(checkboxes[checkbox], 0, wx.EXPAND)
        checkbox_panel.SetSizer(gridsizer)

        checkbox_sizer.Add(checkbox_panel, 0, wx.ALIGN_CENTER)
        checkbox_sizer.AddStretchSpacer(1)

        lower_panel.SetSizer(checkbox_sizer)



        # add all elements to main sizer
        main_sizer.Add(title_panel,  wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(lower_panel,  wx.ID_ANY, wx.EXPAND | wx.ALL)

        # set window border
        self.SetWindowStyle(wx.BORDER_SIMPLE)
