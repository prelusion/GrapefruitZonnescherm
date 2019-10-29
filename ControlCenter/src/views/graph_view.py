import random

from src import mvc
import wxmplot
import wx


class GraphView(wxmplot.PlotPanel):
    def __init__(self, parent):
        super().__init__(parent, pos=(150, 150))
        self.x = []
        self.y = []

        self.SetTestData()
        self.oplot(self.x, self.y, side='left', ymin=0, linewidth=1, labelfontsize=6, legendfontsize=6, autoscale=True, framecolor="LightGrey")
        self.Show()

    def SetData(self, x, y):
        self.x = x
        self.y = y

    def SetTestData(self):
        x = []
        y = []
        for i in range(30):
            x.append(i)
            y.append(random.randint(1,30))
        self.SetData(self.x, self.y)

"""
app = wx.App(redirect=True)
frame = wx.Frame(None, title="Test", size=(1500,900))
frameSizer = wx.GridSizer(1,2,1,1)
graphPanelSizer = wx.GridSizer(2,1,1,1)
frame.SetSizer(frameSizer)
panel = wx.Panel(parent=frame)
panel.SetSizer(graphPanelSizer)
bottomPanel = wx.Panel(parent=frame)
bottomPanel.SetBackgroundColour(colour=(0,255,0))
panel.SetBackgroundColour(colour=(255,0,0))
frameSizer.Add(panel, 0, wx.EXPAND, 0)
graph = GraphView(frame)
graphPanelSizer.Add(graph, 0 ,wx.EXPAND,0)
graphPanelSizer.Add(bottomPanel, 0 , wx.EXPAND, 0)
frame.Show()
app.MainLoop()

#app = wx.App(redirect=True)
#top = wx.Frame(None, title="Hello World", size=(300, 200))
#top.Show()
#app.MainLoop()
"""