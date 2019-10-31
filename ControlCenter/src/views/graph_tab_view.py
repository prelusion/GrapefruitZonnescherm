from src.mvc import View
from src.views import graph_view
import wx

class graph_tab_view(View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(colour=(255,0,0))
        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        self.tab_panel = wx.Notebook(self)
        self.temps_tab = wx.Panel(self.tab_panel)
        self.status_tab = wx.Panel(self.tab_panel)
        self.light_tab = wx.Panel(self.tab_panel)
        self.tab_panel.SetBackgroundColour(colour=(0,255,0))

        self.tab_panel.AddPage(self.temps_tab, "Temps")
        self.tab_panel.AddPage(self.status_tab, "Status")
        self.tab_panel.AddPage(self.light_tab, "Light")


        self.sizer.Add(self.tab_panel, 1, wx.EXPAND)

        self.sizer.Add(self.)
        self.temp_view = graph_view.GraphView(self.temps_tab)
        self.status_view = graph_view.GraphView(self.status_tab)
        self.light_view = graph_view.GraphView(self.light_tab)

class graph_tab(View):
    def __init__(self):


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Test", size=(600, 400))
    sizer = wx.GridSizer(1,1,1,1)
    frame.SetSizer(sizer)
    #frame.Show()
    graph_tab = graph_tab_view(frame)
    sizer.Add(graph_tab,1 , wx.EXPAND)
    #graph_tab.SetSize(300,300)
    frame.Show()
    app.MainLoop()