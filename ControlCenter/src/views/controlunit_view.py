import wx


# size: size=(450, 100)


class ControlUnitView(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Create main panel for control unit
        main_panel = wx.Panel(self, style=wx.BORDER_RAISED, size=(500, 120))
        grid = wx.GridSizer(2, 3, 0, 0)  # Add gridsizer to main panel, 2 rows, 3 columns, 0 borders
        main_panel.SetSizer(grid)

        panels = ("name", "temperature", "status", "color", "connection", "mode")
        for i in panels:
            panel = wx.Panel(main_panel, style=wx.SUNKEN_BORDER)
            panel.SetBackgroundColour((255, 255, 255))
            self.name_label = wx.StaticText(panel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
            self.name_label.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer.Add(self.name_label, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)
            v_sizer.Add(h_sizer, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)
            panel.SetSizer(v_sizer)
            grid.Add(panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

        main_panel.Layout()

    def set_temperature(self, temp):
        return
        self.temp_label.SetLabelText(str(temp))

    def set_name(self, name):
        return
        self.name_label.SetLabelText(str(name))

    def set_status(self, status):
        return
        self.status_label.SetLabelText(str(status))

    def set_device_color(self, color_tuple):
        return
        self.color_panel.SetBackgroundColour(color_tuple)

    def set_connection(self, connection):
        return
        self.connection_label.SetLabelText(str(connection))

    def set_mode(self, mode):
        return
        self.mode_label.SetLabelText(str(mode))
