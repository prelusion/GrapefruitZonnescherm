import os

import wx
from src import const
from src import mvc


class TabView(mvc.View):

    COLOR_INACTIVE = (255, 255, 255)
    COLOR_ACTIVE = (200, 200, 200)

    def __init__(self, parent):
        super().__init__(parent)

        self.SetBackgroundColour((121, 122, 122))

        tab_sizer = wx.GridSizer(1, 3, 0, 0)
        self.SetSizer(tab_sizer)

        manual_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Manual Control")
        manual_tab.SetBackgroundColour(self.COLOR_INACTIVE)
        self.manual_tab = manual_tab

        graph_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Statistics")
        graph_tab.SetBackgroundColour(self.COLOR_INACTIVE)
        self.graph_tab = graph_tab

        settings_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Settings")
        settings_tab.SetBackgroundColour(self.COLOR_INACTIVE)
        self.settings_tab = settings_tab

        tab_sizer.Add(manual_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(graph_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(settings_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)

        icon0 = wx.Bitmap(os.path.join(const.ICONS_DIR, "manual.ico"), wx.BITMAP_TYPE_ICO)
        icon1 = wx.Bitmap(os.path.join(const.ICONS_DIR, "graphs.ico"), wx.BITMAP_TYPE_ICO)
        icon2 = wx.Bitmap(os.path.join(const.ICONS_DIR, "settings.ico"), wx.BITMAP_TYPE_ICO)

        # manual_tab.SetBitmap(icon0)
        # graph_tab.SetBitmap(icon1)
        # settings_tab.SetBitmap(icon2)

        self.set_manual_active()

    def set_manual_active(self):
        self.manual_tab.SetBackgroundColour(self.COLOR_ACTIVE)
        self.graph_tab.SetBackgroundColour(self.COLOR_INACTIVE)
        self.settings_tab.SetBackgroundColour(self.COLOR_INACTIVE)

    def set_graph_active(self):
        self.manual_tab.SetBackgroundColour(self.COLOR_INACTIVE)
        self.graph_tab.SetBackgroundColour(self.COLOR_ACTIVE)
        self.settings_tab.SetBackgroundColour(self.COLOR_INACTIVE)

    def set_settings_active(self):
        self.manual_tab.SetBackgroundColour(self.COLOR_INACTIVE)
        self.graph_tab.SetBackgroundColour(self.COLOR_INACTIVE)
        self.settings_tab.SetBackgroundColour(self.COLOR_ACTIVE)
