import wx

from src import mvc


# label = wx.StaticText(left_panel, wx.ID_ANY, label="test", style=wx.ALIGN_CENTER)
# left_panel_sizer.Add(label, wx.ID_ANY, wx.EXPAND | wx.ALL)


class TopView(mvc.View):

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((255, 0, 0))

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(main_sizer)

        # Left panel
        left_panel = wx.Panel(self)
        left_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_panel.SetSizer(left_panel_sizer)
        left_panel.SetBackgroundColour((0, 255, 0))

        # Right panel
        right_panel = wx.Panel(self)
        right_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        right_panel.SetSizer(right_panel_sizer)
        right_panel.SetBackgroundColour((0, 0, 255))

        main_sizer.Add(left_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(right_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

        main_sizer.Layout()
        self.Layout()
