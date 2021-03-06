import enum

import wx
import wxmplot

from src import mvc


class GraphMode(enum.Enum):
    Temp = 1
    Status = 2
    Light = 3


class Graph(wxmplot.PlotPanel):
    def __init__(self, parent):
        super().__init__(parent, messenger=lambda text, panel: None, show_config_popup=False)


class GraphView(mvc.View):
    def __init__(self, parent, graphmode: GraphMode):
        super().__init__(parent)
        self.parent = parent

        self.graph = Graph(self)
        self.graph.set_xlabel("Time")
        self.graph_sizer = wx.GridSizer(1, 1, 1, 1)
        self.SetSizer(self.graph_sizer)
        self.graph_sizer.Add(self.graph, 0, wx.EXPAND | wx.ALL, 0)

        self.framecolor = "LightGrey"
        self.graphmode = graphmode
        self.linewidth = 2
        self.units = {}
        self.lines = None
        self.index = 0

        if graphmode == GraphMode.Temp:
            self.graph.set_xlabel("Time")
            self.y_min = -64
            self.y_max = 63
            self.graph.set_ylabel("Temperature in °C")
            self.measure_unit = "Temperature in °C"
            self.autoscale = False

        if graphmode == GraphMode.Status:
            self.linewidth = 20
            self.graph.set_xlabel("Time")
            self.y_min = 0
            self.y_max = 1
            self.graph.set_ylabel("Down <-----------> Up")
            self.measure_unit = "Down <-----------> Up"
            self.autoscale = False

        if graphmode == GraphMode.Light:
            self.graph.set_xlabel("Time")
            self.y_min = 0
            self.y_max = 100
            self.graph.set_ylabel("% Light intensity of threshold")
            self.measure_unit = "% Light intensity of threshold"
            self.autoscale = False

    def update_graph(self, device_id, color, timestamps, measurements):
        if device_id not in self.units:
            self.index = 0
            self.lines = self.graph.plot(ydata=measurements,
                                         xdata=timestamps,
                                         ymin=self.y_min,
                                         ymax=self.y_max,
                                         ylabel=self.measure_unit,
                                         side='left',
                                         linewidth=self.linewidth,
                                         labelfontsize=6,
                                         xlabel="Time",
                                         legendfontsize=6,
                                         autoscale=self.autoscale,
                                         framecolor=self.framecolor,
                                         use_dates=True,
                                         color=color),

            self.units[device_id] = self.index
            self.index += 1
        else:
            self.graph.oplot(
                ydata=measurements,
                xdata=timestamps,
                xlabel="Time",
                side='left',
                linewidth=1,
                color=color)

    def clear_graph(self):
        self.graph.clear()
        self.graph.draw()
