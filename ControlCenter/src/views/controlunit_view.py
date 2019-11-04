from collections import namedtuple

import wx

UnitValueBox = namedtuple("UnitValueBox", ["panel", "label"])


class ControlUnitView(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.main_panel = wx.Panel(self, style=wx.BORDER_RAISED, size=(500, 120))
        self.grid = wx.GridSizer(2, 3, 0, 0)  # Add gridsizer to main panel, 2 rows, 3 columns, 0 borders
        self.main_panel.SetSizer(self.grid)

        self.box = {
            "name": None,
            "temperature": None,
            "status": None,
            "color": None,
            "connection": None,
            "mode": None,
        }

        for name in self.box.keys():
            panel = wx.Panel(self.main_panel, style=wx.SUNKEN_BORDER)
            panel.SetBackgroundColour((255, 255, 255))

            label = wx.StaticText(panel, wx.ID_ANY, label="", style=wx.ALIGN_CENTER)

            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)

            h_sizer.Add(label, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)
            v_sizer.Add(h_sizer, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)

            panel.SetSizer(v_sizer)

            self.grid.Add(panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
            self.box[name] = UnitValueBox(panel, label)

        self.grid.Layout()
        self.main_panel.Layout()

    def set_temperature(self, value):
        box = self.box["temperature"]
        box.label.SetLabelText(str(value))
        self._refresh(box.panel)

    def set_name(self, value):
        box = self.box["name"]
        box.label.SetLabelText(str(value))
        self._refresh(box.panel)

    def set_shutter_status(self, value):
        box = self.box["status"]
        box.label.SetLabelText(str(value))
        self._refresh(box.panel)

    def set_device_color(self, value):
        panel = self.box["color"].panel
        panel.SetBackgroundColour(value)
        self._refresh(panel)

    def set_connection(self, value):
        box = self.box["connection"]
        box.label.SetLabelText(str(value))
        self._refresh(box.panel)

    def set_mode(self, value):
        box = self.box["mode"]
        box.label.SetLabelText(str(value))
        self._refresh(box.panel)

    def _refresh(self, panel):
        panel.Layout()
