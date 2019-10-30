import wx

from src import mvc


class ControlUnitsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.units = {}
        self.unit_count = 0

        self.SetBackgroundColour((0, 255, 0))
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)

    def render_unit(self, id_, view):
        print("RENDER CONTROL UNIT:", id_)

        self.unit_count += 1
        btn = wx.Button(self, label="Hi")
        self.vbox.Add(btn, 0, wx.ALL, 5)

        self.Layout()
        self.parent.Layout()
        self.parent.sizer.Layout()
        self.vbox.Layout()

    def remove_unit(self, id_):
        print("REMOVE UNIT:", id_)

        self.vbox.Hide(self.unit_count-1)
        self.vbox.Remove(self.unit_count-1)
        self.unit_count -= 1
