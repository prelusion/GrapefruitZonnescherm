from src import mvc
import wx


class TabView(mvc.View):

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((121, 122, 122))

        tab_sizer = wx.GridSizer(1, 3, 0, 0)
        self.SetSizer(tab_sizer)

        manual_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Manual Control")
        manual_tab.SetBackgroundColour((255, 255, 255))

        graph_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Graph")
        graph_tab.SetBackgroundColour((255, 2550, 255))

        settings_tab = wx.Button(self, style=wx.BORDER_RAISED, label="Settings")
        settings_tab.SetBackgroundColour((255, 255, 255))

        tab_sizer.Add(manual_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(graph_tab,  wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(settings_tab,  wx.ID_ANY, wx.EXPAND | wx.ALL)

    def open_man_tab(self):
        print("test")

    def open_view_tab(self):
        pass

    def open_settings_tab(self):
        pass

