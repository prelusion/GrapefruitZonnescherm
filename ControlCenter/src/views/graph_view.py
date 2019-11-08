import datetime
import enum
import random

import wx
import wxmplot

from src import mvc
from src.measurement import Measurement


class GraphMode(enum.Enum):
    Temp = 1
    Status = 2
    Light = 3


class GraphView(mvc.View):
    def __init__(self, parent, graphmode: GraphMode):
        super().__init__(parent)
        self.graph = Graph(self)
        self.graph_sizer = wx.GridSizer(1, 1, 1, 1)
        self.SetSizer(self.graph_sizer)
        self.graph_sizer.Add(self.graph, 0, wx.EXPAND | wx.ALL, 0)
        self.framecolor = "LightGrey"
        self.graphmode = graphmode
        self.units = []
        self.traces = []
        self.draw_num = 0

        if graphmode == GraphMode.Temp:
            self.graph.set_xlabel("test")
            self.y_min = -200
            self.y_max = 200
            self.measure_unit = "Temperature in °C"
            self.autoscale = True

        if graphmode == GraphMode.Status:
            self.y_min = 0
            self.y_max = 1
            self.measure_unit = "Shutter status: Up or Down"
            self.autoscale = False

        if graphmode == GraphMode.Light:
            self.y_min = 0
            self.y_max = 5000
            self.measure_unit = "Light intensity in #TODO"
            # TODO Set light settings
            self.autoscale = True

    def is_drawn(self, id):
        for trace in self.traces:
            if trace[0] == id:
                return True
        return False

    def find_trace_by_id(self, id):
        for trace in self.traces:
            if trace[0] == id:
                return trace[1]

    def update_graph(self):
        first_drawn = True
        for unit in self.units:
            if len(unit["measurements"]) > 1 and unit["selected"]:

                if len(self.traces) < 1:
                    self.graph.plot(ydata=unit["measurements"], xdata = unit["timestamps"], ymin=self.y_min, ymax=self.y_max, ylabel=self.measure_unit,
                                    side='left', linewidth=1, labelfontsize=6,
                                    legendfontsize=6, autoscale=self.autoscale, framecolor=self.framecolor,
                                    use_dates=True,
                                    color=unit["color"])
                else:
                    self.graph.oplot(ydata=unit["measurementx"], xdata=unit["timestamps"], side='left', linewidth=1, color=unit["color"])

    def find_unit(self, id):
        for unit in self.units:
            if unit[id] == id:
                return unit

    def set_units(self, units):
        values = ""
        if self.graphmode == GraphMode.Temp:
            values = "temperatures"
        elif self.graphmode == GraphMode.Light:
            values = "light_intensity"
        elif self.graphmode == GraphMode.Status:
            values = "shutter_status"

        updated_units = []
        for unit in units:
            new_unit = {
                "id":unit["id"],
                "selected":unit["selected"],
                "color":unit["color"],
                "timestamps":unit["timestamps"],
                "measurements":unit[values],
                "tracenum":0
            }
            updated_units.append(new_unit)
        self.units = updated_units



    def toggle_visible(self, id):
        unit = self.find_unit(id)
        unit["visible"] = not unit["visible"]

    def change_color(self, id, color):
        unit = self.find_unit(id)
        unit["color"] = color


class Graph(wxmplot.PlotPanel):
    def __init__(self, parent):
        super().__init__(parent, pos=(150, 150), messenger=output, show_config_popup=False)
        self.Show()


def output(text, panel):
    return


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
