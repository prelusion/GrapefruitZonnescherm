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
    COLOR_ACTIVE = (0, 0, 0)
    COLOR_INACTIVE = (200, 200, 200)

    def __init__(self, parent):
        super().__init__(parent, size=(500, 120))
        self.parent = parent

        self.boxes = {
            "name": None,
            "temperature": None,
            "status": None,
            "color": None,
            "connection": None,
            "mode": None,
        }

        self._select_callback = None
        self._selected = False

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.SetBackgroundColour(self.COLOR_INACTIVE)

        self.box_panel = wx.Panel(self, style=wx.SUNKEN_BORDER)
        self.grid = wx.GridSizer(2, 3, 0, 0)  # Add gridsizer to main panel, 2 rows, 3 columns, 0 borders
        self.box_panel.SetSizer(self.grid)

        self.sizer.Add(self.box_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 2)

        for name in self.boxes.keys():
            panel = wx.Panel(self.box_panel, style=wx.SUNKEN_BORDER)
            panel.SetBackgroundColour((255, 255, 255))

            label = wx.StaticText(panel, wx.ID_ANY, label="", style=wx.ALIGN_CENTER)

            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)

            h_sizer.Add(label, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)
            v_sizer.Add(h_sizer, 0, wx.CENTER)
            v_sizer.Add((0, 0), 1, wx.EXPAND)

            panel.SetSizer(v_sizer)

            panel.Bind(wx.EVT_LEFT_DOWN, self.on_click)
            label.Bind(wx.EVT_LEFT_DOWN, self.on_click)

            self.grid.Add(panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
            self.boxes[name] = UnitValueBox(panel, label)

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)

    def set_temperature(self, value):
        box = self.boxes["temperature"]
        box.label.SetLabelText(str(value) + " °C")
        self._refresh(box.panel)

    def set_name(self, value):
        box = self.boxes["name"]
        box.label.SetLabelText(str(value))
        box.label.GetFont().SetWeight(wx.BOLD)
        self._refresh(box.panel)

    def set_shutter_status(self, value):
        box = self.boxes["status"]
        box.label.SetLabelText(translate_shutter_status(value))
        self._refresh(box.panel)

    def set_device_color(self, value):
        panel = self.boxes["color"].panel
        panel.SetBackgroundColour(value)
        self._refresh(panel)

    def set_connection(self, value):
        box = self.boxes["connection"]
        box.label.SetLabelText(str(value))
        self._refresh(box.panel)

    def set_mode(self, value):
        box = self.boxes["mode"]
        box.label.SetLabelText(str(value))
        self._refresh(box.panel)

    def _refresh(self, panel):
        panel.Layout()

    def set_selected(self, boolean):
        self.SetBackgroundColour(self.COLOR_ACTIVE) if boolean \
            else self.SetBackgroundColour(self.COLOR_INACTIVE)

    def on_click(self, e):
        if self._select_callback:
            self._select_callback(e)
        else:
            self.set_selected(True) if not self._selected else self.set_selected(False)
            self._selected = not self._selected

    def set_on_click_callback(self, callback):
        self._select_callback = callback
