import datetime
import random
import matplotlib
from src import mvc
import wxmplot
import wx
from src import controlunit
from src.controlunit import Measurement
from src.models.controlunit import ControlUnitModel


class GraphView(wxmplot.PlotPanel):
    def __init__(self, parent):
        super().__init__(parent, pos=(150, 150))
        self.framecolor = "LightGrey"
        self.x = []
        self.y = []
        self.controlUnits = []
        self.SetTestData()
        #self.oplot(self.x, self.y, side='left', ymin=0, linewidth=1, labelfontsize=6, legendfontsize=6, autoscale=True, framecolor=self.framecolor, color="Green")
        self.SetTestData()
        self.clear()
        #self.oplot(self.x, self.y, side='left', ymin=0, linewidth=1, labelfontsize=6, legendfontsize=6, autoscale=True, framecolor=self.framecolor, color="Red", drawstyle="steps-pre", marker="diamond")
        self.Show()

    def AddControlUnit(self, controlUnit:ControlUnitModel):
        self.controlUnits.append(controlUnit)

    def SetTestData(self):
        x = []
        y = []
        for i in range(30):
            x.append(i)
            y.append(random.randint(-10,20))
        self.x = x
        self.y = y

        testUnit = ControlUnitModel(1)
        testUnit.set_name("TestUnit")
        testUnit.set_online(True)
        self.controlUnits = []
        for c in range(2):
            measurements = []
            for i in range(100):
                measurements.append(Measurement(timestamp=datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(hours=i)), temperature=random.randint(-10,20), shutter_status=random.randint(0,1), light_sensitivity=0))
            self.controlUnits.append(measurements)

        test = "test"
    def drawControlUnits(self):
        self.test = 0
        for controlunit in self.controlUnits:
            self.drawControlUnit(controlunit)
            counter = 0
            self.test += 1


    def drawControlUnit(self, controlUnit):
        dates = []
        temps = []
        status = []
        xaxis = []
        x = 0

        for measurement in controlUnit:
            #dates.append(matplotlib.dates.date2num(measurement.timestamp))
            time = int(measurement.timestamp)
            dates.append(time)
            temps.append(measurement.temperature)
            status.append(measurement.shutter_status)
            xaxis.append(x)

        test = "test"

        self.plot(dates, temps, side='left', linewidth=1, labelfontsize=6, legendfontsize=6, autoscale=True, framecolor=self.framecolor, use_dates=True)
        #self.plot(dates, status, side='left', ymin=0, linewidth=1, labelfontsize=6, legendfontsize=6, autoscale=True, framecolor=self.framecolor, style="dashed")
        #self.oplot(xaxis, dates, side='left', ymin=0, linewidth=1, labelfontsize=6, legendfontsize=6, autoscale=True, framecolor=self.framecolor)
        #self.plot_many(self.x, self.y, side='left', ymin=0, linewidth=1, labelfontsize=6, legendfontsize=6, autoscale=True, framecolor=self.framecolor)

if __name__ == "__main__":

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
    graph.drawControlUnits()
    graph.SetTestData()
    app.MainLoop()


#app = wx.App(redirect=True)
#top = wx.Frame(None, title="Hello World", size=(300, 200))
#top.Show()
#app.MainLoop()
