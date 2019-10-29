import wx
from src.views.controlunits_view import ControlUnitsView
EVENT_MONEY_CHANGED = "money_changed"
EVENT_CHANGE_MONEY = "change_money"


class MainView(wx.Frame):
    def __init__(self, title):
        super().__init__(None, title=title, size=(1200, 700))

        main_panel = wx.Panel(self)

        main_sizer_hbox = wx.BoxSizer(wx.HORIZONTAL)
        left_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        right_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)

        left_panel = wx.Panel(main_panel)
        left_panel.SetBackgroundColour((1, 1, 1))
        right_panel = wx.Panel(main_panel)
        right_panel.SetBackgroundColour((0, 0, 255))

        controlunits_view = ControlUnitsView(right_panel)
        right_panel_sizer_vbox.Add(controlunits_view, wx.ID_ANY, wx.EXPAND | wx.ALL)

        left_panel.SetSizer(left_panel_sizer_vbox)
        right_panel.SetSizer(right_panel_sizer_vbox)

        main_sizer_hbox.Add(left_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer_hbox.Add(right_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

        main_panel.SetSizer(main_sizer_hbox)


def mainloop():
    app = wx.App(False)
    mainview = MainView("Grapefruit controlpanel")
    mainview.Show()
    app.MainLoop()


if __name__ == "__main__":
    mainloop()

# self.Bind(wx.EVT_CLOSE, self.OnClose)
# # self.SetIcon(wx.Icon(os.path.join(const.ROOT_DIR, "Assets", "Icons", "logo.ico")))
#
# mainpanel = wx.Panel(self)
# mainsizer = wx.BoxSizer(wx.HORIZONTAL)
#
# # cu panel
# cupanel = wx.Panel(mainpanel)
# cupanel.SetBackgroundColour((1, 1, 1))
# cupanel.Show()
# cupanel.Layout()
# # data panel
# datapanel = wx.Panel(mainpanel)
# datapanel.SetBackgroundColour((100, 100, 100))
# datapanel.Show()
# datapanel.Layout()
# datapanel_sizer = wx.BoxSizer(wx.VERTICAL)
#
# controlunits_view = ControlUnitsView(mainpanel)
#
# datapanel_sizer.Add(controlunits_view, wx.ID_ANY, wx.EXPAND | wx.ALL)
# #
# datapanel.SetSizer(datapanel_sizer)
# datapanel.Layout()
#
# # main sizer
# mainsizer.Add(cupanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
# mainsizer.Add(datapanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
#
# mainpanel.SetSizer(mainsizer)
# mainpanel.Layout()
