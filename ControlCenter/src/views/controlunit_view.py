import wx
from collections import namedtuple


UnitValueBox = namedtuple("UnitValueBox", ["panel", "label"])


class ControlUnitView(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)

        main_panel = wx.Panel(self, style=wx.BORDER_RAISED, size=(500, 120))
        grid = wx.GridSizer(2, 3, 0, 0)  # Add gridsizer to main panel, 2 rows, 3 columns, 0 borders
        main_panel.SetSizer(grid)

        self.panels = {
            "name": None,
            "temperature": None,
            "status": None,
            "color": None,
            "connection": None,
            "mode": None,
        }

        for name in self.panels.keys():
            panel = wx.Panel(main_panel, style=wx.SUNKEN_BORDER)
            panel.SetBackgroundColour((255, 255, 255))
            label = wx.StaticText(panel, wx.ID_ANY, label="", style=wx.ALIGN_CENTER)
            label.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer.Add(label, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)
            v_sizer.Add(h_sizer, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)
            panel.SetSizer(v_sizer)
            grid.Add(panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
            self.panels[name] = UnitValueBox(panel, label)

        grid.Layout()
        main_panel.Layout()

    def set_temperature(self, temp):
        self.panels["temperature"].label.SetLabelText(str(temp))

    def set_name(self, name):
        self.panels["name"].label.SetLabelText(str(name))

    def set_status(self, status):
        self.panels["status"].label.SetLabelText(str(status))

    def set_device_color(self, color_tuple):
        self.panels["color"].panel.SetBackgroundColour(color_tuple)

    def set_connection(self, connection):
        self.panels["connection"].label.SetLabelText(str(connection))

    def set_mode(self, mode):
        self.panels["mode"].label.SetLabelText(str(mode))
