import datetime
import random
import matplotlib
from src import mvc
import wxmplot
import wx
from src import controlunit
from src.controlunit import Measurement
from src.models.controlunit import ControlUnitModel


class GraphView(mvc.View):
    def __init__(self, parent, title, unit):
        super().__init__(parent)
        self.measure_unit = unit
        self.graph = Graph(self)
        self.graph_sizer = wx.GridSizer(1, 1, 1, 1)
        self.SetSizer(self.graph_sizer)
        self.graph_sizer.Add(self.graph, 0, wx.EXPAND, 0)

        self.framecolor = "LightGrey"
        self.units = []
        self.x_max = 0
        self.y_min = -20
        self.y_max = 40

    def update_graph(self):
        dates = []
        temps = []
        status = []
        xdata = []
        x = 0

        first_drawn = True
        for unit in self.units:
            if unit["visible"]:
                for measurement in unit["measurements"]:
                    time = int(measurement.timestamp)
                    dates.append(time)
                    temps.append(measurement.temperature)
                    status.append(measurement.shutter_status)
                    xdata.append(x)
                if first_drawn:
                    self.graph.plot(dates, temps, ylabel=self.measure_unit , side='left', linewidth=1, labelfontsize=5,
                                    legendfontsize=6, autoscale=True, framecolor=self.framecolor, use_dates=True,
                                    color=unit["color"])
                else:
                    self.graph.oplot(dates, temps, side='left', linewidth=1, color=unit["color"])

    def find_unit(self, id):
        for unit in self.units:
            if unit[id] == id:
                return unit

    def set_unit(self, id, measurements):
        new_unit = {
            "id": id,
            "measurements": measurements,
            "color": "Green",
            "visible": True,
        }
        for unit in self.units:
            if unit[id] == id:
                unit = new_unit
                return
        self.units.append(new_unit)

    def toggle_visible(self, id):
        unit = self.find_unit(id)
        unit["visible"] = not unit["visible"]

    def change_color(self, id, color):
        unit = self.find_unit(id)
        unit["color"] = color


class Graph(wxmplot.PlotPanel):
    def __init__(self, parent):
        super().__init__(parent, pos=(150, 150))
        self.Show()


# For testing purposes, please ignore
def update():
    graph.update()


def SetTestData(graph_view: GraphView):
    measurements = []
    temp = 20.000
    for i in range(100):
        temp += random.uniform(-3, 3)
        measurements.append(
            Measurement(timestamp=datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(hours=i)),
                        temperature=temp, shutter_status=random.randint(0, 1), light_intensity=0))
    graph_view.set_unit(1, measurements)


if __name__ == "__main__":
    app = wx.App(redirect=True)
    frame = wx.Frame(None, title="Test", size=(1500, 900))
    frameSizer = wx.GridSizer(1, 2, 1, 1)
    graphPanelSizer = wx.GridSizer(2, 1, 1, 1)
    frame.SetSizer(frameSizer)
    panel = wx.Panel(parent=frame)
    panel.SetSizer(graphPanelSizer)
    bottomPanel = wx.Panel(parent=frame)
    bottomPanel.SetBackgroundColour(colour=(0, 255, 0))
    panel.SetBackgroundColour(colour=(255, 0, 0))
    frameSizer.Add(panel, 0, wx.EXPAND, 0)
    graph = GraphView(frame)
    graphPanelSizer.Add(graph, 0, wx.EXPAND, 0)
    graphPanelSizer.Add(bottomPanel, 0, wx.EXPAND, 0)
    frame.Show()
    SetTestData(graph)
    graph.update_graph()
    app.MainLoop()

# app = wx.App(redirect=True)
# top = wx.Frame(None, title="Hello World", size=(300, 200))
# top.Show()
# app.MainLoop()
