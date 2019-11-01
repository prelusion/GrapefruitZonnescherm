import wx


class CenteredLabel(wx.Panel):
    def __init__(self, parent, label):
        super().__init__(parent)

        label = wx.StaticText(self, wx.ID_ANY, label=label, style=wx.ALIGN_CENTER)

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        v_sizer = wx.BoxSizer(wx.VERTICAL)

        h_sizer.Add(label, 0, wx.CENTER)
        v_sizer.Add((0, 0), 1, wx.EXPAND)
        v_sizer.Add(h_sizer, 0, wx.CENTER)
        v_sizer.Add((0, 0), 1, wx.EXPAND)

        self.SetSizer(v_sizer)
