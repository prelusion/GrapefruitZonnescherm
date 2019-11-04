from collections import namedtuple

import wx

UnitValueBox = namedtuple("UnitValueBox", ["panel", "label"])


def translate_shutter_status(value):
    distributor = {
        None: "unknown",
        0: "up",
        1: "down",
        2: "going up",
        4: "going down"
    }
    return distributor[value]


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

            infolabel = wx.StaticText(panel, wx.ID_ANY, label="Info label", style=wx.ALIGN_CENTER)
            infolabel.SetLabelText(name)
            datalabel = wx.StaticText(panel, wx.ID_ANY, label="Data label", style=wx.ALIGN_CENTER)

            vertical_sizer = wx.BoxSizer(wx.VERTICAL)

            vertical_sizer.Add(infolabel, 0, wx.CENTER)
            vertical_sizer.Add(datalabel,  0, wx.CENTER)

            panel.SetSizer(vertical_sizer)

            self.grid.Add(panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
            self.box[name] = UnitValueBox(panel, datalabel)

        self.grid.Layout()
        self.main_panel.Layout()

    def set_temperature(self, value):
        box = self.box["temperature"]
        box.label.SetLabelText(str(value) + " °C")
        self._refresh(box.panel)

    def set_name(self, value):
        box = self.box["name"]
        box.label.SetLabelText(str(value))
        box.label.GetFont().SetWeight(wx.BOLD)
        self._refresh(box.panel)

    def set_shutter_status(self, value):
        box = self.box["status"]
        box.label.SetLabelText(translate_shutter_status(value))
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
