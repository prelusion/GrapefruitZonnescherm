import os

import wx
import const
from src import mvc


class TabView(mvc.View):

    def __init__(self, parent):
        super().__init__(parent)

        self.SetBackgroundColour((121, 122, 122))

        tab_sizer = wx.GridSizer(1, 3, 0, 0)
        self.SetSizer(tab_sizer)

        manual_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Manual Control")
        manual_tab.SetBackgroundColour((255, 255, 255))
        self.manual_tab = manual_tab

        graph_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Statistics")
        graph_tab.SetBackgroundColour((255, 2550, 255))
        self.graph_tab = graph_tab

        settings_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Settings")
        settings_tab.SetBackgroundColour((255, 255, 255))
        self.settings_tab = settings_tab

        tab_sizer.Add(manual_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(graph_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(settings_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)

        icon0 = wx.Bitmap(os.path.join(const.ICONS_DIR, "manual.ico"), wx.BITMAP_TYPE_ICO)
        icon1 = wx.Bitmap(os.path.join(const.ICONS_DIR, "graphs.ico"), wx.BITMAP_TYPE_ICO)
        icon2 = wx.Bitmap(os.path.join(const.ICONS_DIR, "settings.ico"), wx.BITMAP_TYPE_ICO)

        manual_tab.SetBitmap(icon0)
        graph_tab.SetBitmap(icon1)
        settings_tab.SetBitmap(icon2)
