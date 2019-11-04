import wx
import wx.lib.scrolledpanel as scrolled

from src.views.controlunit_view import ControlUnitView


class ControlUnitsView(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.unit_views = {}
        self.unit_indexes = {}
        self.unit_count = 1  # begins at 1 because the spacer is at the first index

        self.SetBackgroundColour((173, 166, 166))

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.unit_sizer = wx.BoxSizer(wx.VERTICAL)
        self.unit_sizer.AddSpacer(20)

        self.main_sizer.Add(self.unit_sizer, 0, wx.CENTER, border=50)
        self.SetSizer(self.main_sizer)

    def render_unit(self, id_, view):
        # view.SetBackgroundColour((255, 0, 255))
        self.unit_views[id_] = view
        self.unit_sizer.Add(view, 0, wx.EXPAND | wx.ALL, 10)
        self.unit_indexes[id_] = self.unit_count
        self.unit_sizer.Layout()
        self.unit_count += 1
        self.main_sizer.Layout()
        self.SetupScrolling()

    def remove_unit(self, id_):
        idx = self.unit_indexes[id_]
        self.unit_sizer.Hide(self.unit_indexes[id_])
        self.unit_sizer.Remove(self.unit_indexes[id_])
        self.unit_count -= 1
        del self.unit_views[id_]
        self._update_indexes(idx)
        self.unit_sizer.Layout()
        self.SetupScrolling()

    def _update_indexes(self, removed_index):
        for i, id_ in enumerate(self.unit_indexes):
            if self.unit_indexes[id_] > removed_index:
                self.unit_indexes[id_] -= 1
