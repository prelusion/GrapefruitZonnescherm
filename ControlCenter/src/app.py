import wx
import os
from src import const

EVENT_MONEY_CHANGED = "money_changed"
EVENT_CHANGE_MONEY = "change_money"


class MainView(wx.Frame):
    def __init__(self, title):
        super().__init__(None, title=title, size=(1200, 700))

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.SetIcon(wx.Icon(os.path.join(const.ROOT_DIR, "Assets", "Icons", "logo.ico")))

        mainpanel = wx.Panel(self)
        grid = wx.GridSizer(0, 2, 0, 0)
        mainpanel.SetSizer(grid)
        mainpanel.Layout()

        cupanel = wx.Panel(mainpanel)
        cupanel.SetBackgroundColour((1, 1, 1))

        datapanel = wx.Panel(mainpanel)
        datapanel.SetBackgroundColour((100, 100, 100))

        grid.Add(cupanel , 0, wx.EXPAND, 0)
        grid.Add(datapanel, 0, wx.EXPAND, 0)

    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()


def mainloop():
    app = wx.App(False)
    mainview = MainView("Grapefruit controlpanel")
    mainview.Show()
    app.MainLoop()


if __name__ == "__main__":
    mainloop()
