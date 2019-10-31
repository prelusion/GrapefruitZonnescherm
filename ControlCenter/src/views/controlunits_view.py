import random

import wx

from src import mvc
from src.views.controlunit_view import ControlUnitView

UNIT_COLORS = (
    (255, 0, 0),
    (255, 123, 0),
    (87, 6, 253),
    (1, 209, 126),
)


def randcolor():
    return random.choice(UNIT_COLORS)


class ControlUnitsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.units = {}
        self.unit_count = 0

        self.SetBackgroundColour((173, 166, 166))
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

    def render_unit(self, id_, view):
        view.set_device_color(randcolor())
        self.main_sizer.Add(view,  0, wx.CENTER)
        self.units[id_] = self.unit_count
        self.main_sizer.Layout()
        self.unit_count += 1


    def remove_unit(self, id_):
        idx = self.units[id_]
        self.main_sizer.Hide(self.units[id_])
        self.main_sizer.Remove(self.units[id_])
        self.unit_count -= 1
        self._update_indexes(idx)
        self.main_sizer.Layout()

    def _update_indexes(self, removed_index):
        for i, id_ in enumerate(self.units):
            if self.units[id_] > removed_index:
                self.units[id_] -= 1
