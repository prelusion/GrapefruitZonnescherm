import datetime
import os
import random

import wx

from src.controlunit import Measurement
from src.mvc import View
from src.views import graph_view
from src import const


class GraphTabView(View):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        self.tab_panel = wx.Notebook(self)
        self.tab_panel.SetWindowStyle(wx.NB_TOP)

        self.temps_tab = graph_tab(self.tab_panel, graph_view.GraphMode.Temp)
        self.status_tab = graph_tab(self.tab_panel, graph_view.GraphMode.Status)
        self.light_tab = graph_tab(self.tab_panel, graph_view.GraphMode.Light)

        self.tab_panel.AddPage(self.temps_tab, "Temperatures")
        self.tab_panel.AddPage(self.status_tab, "Shutter status")
        self.tab_panel.AddPage(self.light_tab, "Light intensity")

        icons = wx.ImageList(16, 16)
        self.tab_panel.AssignImageList(icons)
        icon0 = icons.Add(wx.Bitmap(os.path.join(const.ICONS_DIR, "small_temp.ico"), wx.BITMAP_TYPE_ICO))
        icon1 = icons.Add(wx.Bitmap(os.path.join(const.ICONS_DIR, "small_status.ico"), wx.BITMAP_TYPE_ICO))
        icon2 = icons.Add(wx.Bitmap(os.path.join(const.ICONS_DIR, "small_light.ico"), wx.BITMAP_TYPE_ICO))
        self.tab_panel.SetPageImage(0, icon0)
        self.tab_panel.SetPageImage(1, icon1)
        self.tab_panel.SetPageImage(2, icon2)

        self.sizer.Add(self.tab_panel, 1, wx.EXPAND)

    def update_graphs(self, units):
        self.temps_tab.graph.set_units(units)
        self.status_tab.graph.set_units(units)
        self.light_tab.graph.set_units(units)
        self.temps_tab.graph.update_graph()


class graph_tab(View):
    def __init__(self, parent, graphmode: graph_view.GraphMode):
        super().__init__(parent)
        self.graph = graph_view.GraphView(self, graphmode)
        sizer = wx.GridSizer(1, 1, 1, 1)
        self.SetSizer(sizer)
        sizer.Add(self.graph, 0, wx.EXPAND | wx.ALL, 0)
        self.SetBackgroundColour(colour=(0, 255, 0))
        self.graph.SetSize(200, 200)
        #TODO Remove test data
        #self.create_test_Data()

    def create_test_Data(self):
        SetTestData(self.graph)
        self.graph.update_graph()

def SetTestData(graph_view: graph_view.GraphView):
    timestamps = []
    temps = []
    status = []
    light = []
    temp = 20.000
    for i in range(2):
        temp += random.uniform(-3, 3)
        temps.append(temp)
        status.append(1)
        light.append(500)
        timestamps.append(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(hours=i)))
    graph_view.temps_tab.graph.set_unit(1, timestamps, temps)


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Test", size=(600, 400))
    sizer = wx.GridSizer(1, 1, 1, 1)
    frame.SetSizer(sizer)
    # frame.Show()
    graph_tab = GraphTabView(frame)
    sizer.Add(graph_tab, 1, wx.EXPAND)
    # graph_tab.SetSize(300,300)
    SetTestData(graph_tab)
    graph_tab.temps_tab.graph.update_graph()
    graph_tab.Update()
    graph_tab.Show()
    frame.Show()
    app.MainLoop()
