from src import mvc
import wx


class TabView(mvc.View):

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((121, 122, 122))

        # Add sizer to tab_panel
        tab_sizer = wx.GridSizer(1, 3, 0, 0)
        self.SetSizer(tab_sizer)

        # Create manual control tab
        manual_tab = wx.Button(self, style=wx.BORDER_RAISED)
        manual_tab.SetBackgroundColour((255, 255, 255))

        # Create label and set font for the label
        manual_label = wx.StaticText(manual_tab, wx.ID_ANY, label="Manual control")
        font = manual_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        manual_label.SetFont(font)

        # align label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(manual_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        manual_tab.SetSizer(main_sizer)

        # Create graph tab
        graph_tab = wx.Button(self, style=wx.BORDER_RAISED)
        graph_tab.SetBackgroundColour((255, 2550, 255))

        # Create label and set font for the label
        graph_label = wx.StaticText(graph_tab, wx.ID_ANY, label="Graph views")
        font = graph_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        graph_label.SetFont(font)

        # align label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(graph_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        graph_tab.SetSizer(main_sizer)

        # Create settings tab
        settings_tab = wx.Button(self, style=wx.BORDER_RAISED)
        settings_tab.SetBackgroundColour((255, 255, 255))

        # Create label and set font for the label
        settings_label = wx.StaticText(settings_tab, wx.ID_ANY, label="Settings")
        font = settings_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        settings_label.SetFont(font)

        # align label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(settings_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        settings_tab.SetSizer(main_sizer)

        # Add all panels to tabview
        tab_sizer.Add(manual_tab, wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(graph_tab,  wx.ID_ANY, wx.EXPAND | wx.ALL)
        tab_sizer.Add(settings_tab,  wx.ID_ANY, wx.EXPAND | wx.ALL)

    def open_man_tab(self):
        print("test")

    def open_view_tab(self):
        pass

    def open_settings_tab(self):
        pass

