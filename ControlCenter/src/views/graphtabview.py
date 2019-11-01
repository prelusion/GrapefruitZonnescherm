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


class graph_tab(View):
    def __init__(self, parent, graphmode: graph_view.GraphMode):
        super().__init__(parent)
        graph = graph_view.GraphView(self, graphmode)
        sizer = wx.GridSizer(1, 1, 1, 1)
        self.SetSizer(sizer)
        sizer.Add(graph, 0, wx.EXPAND, 0)
        self.SetBackgroundColour(colour=(0, 255, 0))
        graph.SetSize(200, 200)
        SetTestData(graph)
        graph.update_graph()


def SetTestData(graph_view: graph_view.GraphView):
    measurements = []
    temp = 20.000
    for i in range(100):
        temp += random.uniform(-3, 3)
        measurements.append(
            Measurement(timestamp=datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(hours=i)),
                        temperature=temp, shutter_status=random.randint(0, 1), light_intensity=0))
    graph_view.set_unit(1, measurements)


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Test", size=(600, 400))
    sizer = wx.GridSizer(1, 1, 1, 1)
    frame.SetSizer(sizer)
    # frame.Show()
    graph_tab = GraphTabView(frame)
    sizer.Add(graph_tab, 1, wx.EXPAND)
    # graph_tab.SetSize(300,300)
    frame.Show()
    app.MainLoop()
