import wx

from src import mvc
from src import widgets


class TopView(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(main_sizer)

        # Left panel
        left_panel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        left_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_panel.SetSizer(left_panel_sizer)

        label = widgets.CenteredLabel(left_panel, "RICK ZIJN MOEDER")
        left_panel_sizer.Add(label, wx.ID_ANY, wx.EXPAND | wx.ALL)

        # Right panel
        right_panel = wx.Panel(self, style=wx.BORDER_SUNKEN)
        right_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel.SetSizer(right_panel_sizer)

        main_sizer.Add(left_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(right_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)



