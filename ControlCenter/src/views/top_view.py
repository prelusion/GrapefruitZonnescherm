import wx

from src import widgets
from src.controllers.tabview_controller import TabviewController


class TopView(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(main_sizer)

        # Left panel
        left_panel = wx.Panel(self)
        left_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_panel.SetSizer(left_panel_sizer)

        label = widgets.CenteredLabel(left_panel, "Devices")
        label.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        left_panel_sizer.Add(label, wx.ID_ANY, wx.EXPAND | wx.ALL)

        # Right panel
        right_panel = wx.Panel(self)
        right_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel.SetSizer(right_panel_sizer)

        self.tab_view_controller = TabviewController(right_panel)
        right_panel_sizer.Add(self.tab_view_controller.view, 1, wx.EXPAND | wx.ALL)

        main_sizer.Add(left_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(right_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

        self.Layout()
