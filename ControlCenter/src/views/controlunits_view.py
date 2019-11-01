import random

import wx
from src.views.controlunit_view import ControlUnitView

from src import mvc
import wx.lib.scrolledpanel as scrolled


class ControlUnitsView(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.units = {}
        self.unit_count = 1  # begins at 1 because the spacer is at the first index

        self.SetBackgroundColour((173, 166, 166))

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.unit_sizer = wx.BoxSizer(wx.VERTICAL)
        self.unit_sizer.AddSpacer(20)

        self.main_sizer.Add(self.unit_sizer, 0, wx.CENTER, border=50)
        self.SetSizer(self.main_sizer)

        debug = False
        if debug:
            for i in range(3):
                view = ControlUnitView(self)
                self.render_unit(1, view)


    def render_unit(self, id_, view):
        print("render unit:", id_)
        self.unit_sizer.Add(view, 0, wx.EXPAND | wx.ALL, 10)
        self.units[id_] = self.unit_count
        self.unit_sizer.Layout()
        self.unit_count += 1
        self.main_sizer.Layout()
        self.SetupScrolling()

    def remove_unit(self, id_):
        print("remove unit:", id_)
        idx = self.units[id_]
        self.unit_sizer.Hide(self.units[id_])
        self.unit_sizer.Remove(self.units[id_])
        self.unit_count -= 1
        self._update_indexes(idx)
        self.unit_sizer.Layout()
        self.SetupScrolling()

    def _update_indexes(self, removed_index):
        for i, id_ in enumerate(self.units):
            if self.units[id_] > removed_index:
                self.units[id_] -= 1
