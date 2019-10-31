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
        self.x_max =  0
        self.y_min = -20
        self.y_max = 40
        self.show_temps = True
        self.show_status = False
        self.controlUnits = []
        self.SetTestData()
        self.Show()

    def update(self):
        self.SetTestData()
        self.update()
        s

    def toggle_show_temps(self):
        self.show_temps is not self.show_temps

    def toggle__show_status(self):
        self.show_status is not self.show_status

    def add_controlUnit(self, controlUnit:ControlUnitModel):
        self.controlUnits.append(controlUnit)

    def del_ontrolUnit(self, id):
        for controlUnit in self.controlUnits:
            if controlUnit.get_id == id:
                self.controlUnits.remove(controlUnit)

    def get_controlUnit(self, id):
        for controlUnit in self.controlUnits:
            if controlUnit.get_id == id:
                return controlUnit
    def get_controlUnits(self):
        return self.controlUnits

    def SetTestData(self):
        testUnit = ControlUnitModel(1)
        testUnit.set_name("TestUnit")
        testUnit.set_online(True)
        self.controlUnits = []
        for c in range(1):
            for i in range(100):
                testUnit.add_measurement(Measurement(timestamp=datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(hours=i)), temperature=random.uniform(-10,20), shutter_status=random.randint(0,1), light_sensitivity=0))
        self.add_controlUnit(testUnit)

    def drawControlUnits(self):
        for controlunit in self.controlUnits:
            self.drawControlUnit(controlunit)



    def drawControlUnit(self, control_unit:ControlUnitModel, temp = True,status = False, light = False ):
        measurements = control_unit.get_measurements()
        dates = []
        temps = []
        status = []
        xdata = []
        x = 0

        for measurement in measurements.get():
            time = int(measurement.timestamp)
            dates.append(time)
            temps.append(measurement.temperature)
            status.append(measurement.shutter_status)
            xdata.append(x)

        first_drawn = True
        if temp:
            self.plot(dates, temps, ylabel="Temperature in °C", side='left', linewidth=1, labelfontsize=5,
                      legendfontsize=6, autoscale=True, framecolor=self.framecolor, use_dates=True,
                      color=control_unit.get_colour())
            first_drawn = False

        if status:
            if first_drawn:
                self.plot(dates, status, style="dotted", side='left', linewidth=1, labelfontsize=5, legendfontsize=6,
                        autoscale=True, framecolor=self.framecolor, use_dates=True, color=control_unit.get_colour())
            else:
                self.oplot(dates, status, style="dotted", side='left', linewidth=1, labelfontsize=5, legendfontsize=6,
                        autoscale=True,  use_dates=True, color=control_unit.get_colour())

# For testing purposes, please ignore
def update():
    graph.update()
    

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
    #app.root.after(2000,update)
    #app.MainLoop()
    test = "test"


#app = wx.App(redirect=True)
#top = wx.Frame(None, title="Hello World", size=(300, 200))
#top.Show()
#app.MainLoop()
