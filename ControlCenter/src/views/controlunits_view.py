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

    def render_unit(self, id_, view):
        print("RENDER CONTROL UNIT:", id_)

        self.unit_count += 1
        btn = wx.Button(self, -1, str(id_))
        self.vbox.Add(btn, 0, wx.ALL, 5)
        # self.parent.fSizer().Layout()
        # self.parent.Fit()
        # btn = wx.Button(self, -1, str(id_))
        #
        # self.units[id_] = self.unit_count
        # self.unit_count += 1
        # print("button made")
        # self.vbox.Add(btn, wx.ID_ANY, wx.ALIGN_CENTER)
        # print("add button")

    def remove_unit(self, id_):
        print("REMOVE UNIT:", id_)
        # count = self.units[id_]
        # self.vbox.Remove(count)

