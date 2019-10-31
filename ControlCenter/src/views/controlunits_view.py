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

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour((0, 255, 0))

        # controlunit_view = ControlUnitView(self.parent)
        # self.vbox.Add(controlunit_view, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.vbox)

    def render_unit(self, id_, view):
        # btn = wx.Button(self, label=str(id_))
        # btn.SetBackgroundColour(randcolor())
        self.vbox.Add(view, 0, wx.ALL, 5)
        self.units[id_] = self.unit_count
        self.vbox.Layout()
        self.unit_count += 1

    def remove_unit(self, id_):
        idx = self.units[id_]
        self.vbox.Hide(self.units[id_])
        self.vbox.Remove(self.units[id_])
        self.unit_count -= 1
        self._update_indexes(idx)
        self.vbox.Layout()

    def _update_indexes(self, removed_index):
        for i, id_ in enumerate(self.units):
            if self.units[id_] > removed_index:
                self.units[id_] -= 1
