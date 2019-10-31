import random

import wx

from src import mvc
from src.views.controlunit_view import ControlUnitView

tmp = []
unit_colors = [
    (255, 0, 0),
    (255, 123, 0),
    (87, 6, 253),
    (1, 209, 126),
    (255, 33, 55),
    (21, 130, 10),
    (8, 16, 230),
]


def randcolor():
    global tmp, unit_colors
    result = random.choice(unit_colors)
    tmp.append(result)
    unit_colors.remove(result)
    if len(unit_colors) == 0:
        unit_colors = tmp.copy()
        tmp = []
    return result


class ControlUnitsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.units = {}
        self.unit_count = 0

        self.SetBackgroundColour((173, 166, 166))

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

        self.unit_sizer = wx.BoxSizer(wx.VERTICAL)
        self.unit_sizer.AddSpacer(20)

        self.main_sizer.Add(self.unit_sizer, 0, wx.CENTER, border=50)

        debug = True
        if debug:
            self.render_unit(1, ControlUnitView(self))
            self.render_unit(2, ControlUnitView(self))
            self.render_unit(3, ControlUnitView(self))
            self.render_unit(4, ControlUnitView(self))

    def render_unit(self, id_, view):
        view.set_device_color(randcolor())
        self.unit_sizer.Add(view, 0, wx.EXPAND | wx.ALL, 10)
        self.units[id_] = self.unit_count
        self.unit_sizer.Layout()
        self.unit_count += 1

    def remove_unit(self, id_):
        idx = self.units[id_]
        self.unit_sizer.Hide(self.units[id_])
        self.unit_sizer.Remove(self.units[id_])
        self.unit_count -= 1
        self._update_indexes(idx)
        self.unit_sizer.Layout()

    def _update_indexes(self, removed_index):
        for i, id_ in enumerate(self.units):
            if self.units[id_] > removed_index:
                self.units[id_] -= 1
