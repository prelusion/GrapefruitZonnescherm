import os

import wx

from src import const
from src.views.controlunits_view import ControlUnitsView
from src.views.filter_view import FilterView
from src.views.graph_view import GraphView
from src.views.tab_view import TabView


class MainView(wx.Frame):
    def __init__(self, title):
        super().__init__(None, title=title, size=(1200, 700))

        self.SetIcon(wx.Icon(os.path.join(const.ROOT_DIR, "Assets", "Icons", "logo.ico")))

        main_panel = wx.Panel(self)

        main_sizer_hbox = wx.BoxSizer(wx.HORIZONTAL)
        left_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        right_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)

        left_panel = wx.Panel(main_panel)
        left_panel.SetBackgroundColour((1, 1, 1))
        right_panel = wx.Panel(main_panel)
        right_panel.SetBackgroundColour((0, 0, 255))

        controlunits_view = ControlUnitsView(left_panel)
        filter_view = FilterView(left_panel)

        left_panel_sizer_vbox.Add(controlunits_view, 3, wx.EXPAND | wx.ALL)
        left_panel_sizer_vbox.Add(filter_view, 1, wx.EXPAND | wx.ALL)
        left_panel.SetSizer(left_panel_sizer_vbox)

        tab_view = TabView(right_panel)
        graph_view = GraphView(right_panel)

        right_panel_sizer_vbox.Add(tab_view, 1, wx.EXPAND | wx.ALL)
        right_panel_sizer_vbox.Add(graph_view, 10, wx.EXPAND | wx.ALL)
        right_panel.SetSizer(right_panel_sizer_vbox)

        main_sizer_hbox.Add(left_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer_hbox.Add(right_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

        main_panel.SetSizer(main_sizer_hbox)


def mainloop():
    app = wx.App(False)
    mainview = MainView("Grapefruit controlpanel")
    mainview.Show()
    app.MainLoop()


if __name__ == "__main__":
    mainloop()
