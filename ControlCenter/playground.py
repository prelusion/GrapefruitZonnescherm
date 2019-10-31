import wx


class test(wx.Frame):

    def __init__(self, title):
        super().__init__(None, title=title, size=(607, 100))
        # Create main panel for control unit
        unit = wx.Panel(self, style=wx.BORDER_RAISED)

        main_panel = wx.Panel(unit)
        main_panel.SetBackgroundColour((1,1,1))



app = wx.App(False)
mainview = test("Grapefruit controlpanel")
mainview.Show()
app.MainLoop()


