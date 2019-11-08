import os

import wx

from src import const
from src.mvc import View
from src.views import graph_view


class GraphTab(View):
    def __init__(self, parent, graphmode: graph_view.GraphMode):
        super().__init__(parent)
        self.graph = graph_view.GraphView(self, graphmode)
        sizer = wx.GridSizer(1, 1, 1, 1)
        self.SetSizer(sizer)
        sizer.Add(self.graph, 0, wx.EXPAND | wx.ALL, 0)
        # self.SetBackgroundColour(colour=(0, 255, 0))
        self.graph.SetSize(200, 200)


class GraphTabView(View):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        self.tab_panel = wx.Notebook(self)
        self.tab_panel.SetWindowStyle(wx.NB_TOP)

        self.temps_tab = GraphTab(self.tab_panel, graph_view.GraphMode.Temp)
        self.status_tab = GraphTab(self.tab_panel, graph_view.GraphMode.Status)
        self.light_tab = GraphTab(self.tab_panel, graph_view.GraphMode.Light)

        self.tab_panel.AddPage(self.temps_tab, "Temperatures")
        self.tab_panel.AddPage(self.status_tab, "Shutter status")
        self.tab_panel.AddPage(self.light_tab, "Light intensity")

        # Icons
        icons = wx.ImageList(16, 16)
        self.tab_panel.AssignImageList(icons)
        icon0 = icons.Add(wx.Bitmap(os.path.join(const.ICONS_DIR, "small_temp.ico"), wx.BITMAP_TYPE_ICO))
        icon1 = icons.Add(wx.Bitmap(os.path.join(const.ICONS_DIR, "small_status.ico"), wx.BITMAP_TYPE_ICO))
        icon2 = icons.Add(wx.Bitmap(os.path.join(const.ICONS_DIR, "small_light.ico"), wx.BITMAP_TYPE_ICO))
        self.tab_panel.SetPageImage(0, icon0)
        self.tab_panel.SetPageImage(1, icon1)
        self.tab_panel.SetPageImage(2, icon2)

        self.sizer.Add(self.tab_panel, 1, wx.EXPAND)

    def update_temperature_graph(self, device_id, color, timestamps, temperatures):
        self.temps_tab.graph.update_graph(device_id, color, timestamps, temperatures)

    def remove_device(self, device_id):
        self.temps_tab.graph.remove_device(device_id)

    def update_status_graph(self, device_id, color, timestamps, status):
        self.status_tab.graph.update_graph(device_id, color, timestamps, status)

    def update_light_graph(self, device_id, color, timestamps, light):
        self.light_tab.graph.update_graph(device_id, color, timestamps, light)
