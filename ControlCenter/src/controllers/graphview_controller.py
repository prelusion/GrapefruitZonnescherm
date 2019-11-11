import logging
import threading
import time

import wx

from src import mvc
from src.views.graphtab_view import GraphTabView

logger = logging.getLogger(__name__)


class GraphViewController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.controlunit_manager = controlunit_manager

        self.view = GraphTabView(view_parent)

        self.controlunit_manager.units.add_callback(self.on_controlunits_change)
        self.units = []
        self._mocked = False

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.selected.add_callback(self.on_controlunit_selected_change)

    def redraw_all_units(self):
        self.view.clear_graph()
        for unit in self.controlunit_manager.get_selected_units():
            comm, model = unit
            self.update_graph(model, model.get_measurements())

    def on_controlunit_selected_change(self, model, selected):

        def execute():
            self.redraw_all_units()

            if selected:
                model.measurements.add_callback(self.on_controlunit_measurement_change)
                model.color.add_callback(self.on_controlunit_color_change)
            else:
                try:
                    model.measurements.del_callback(self.on_controlunit_measurement_change)
                    model.color.del_callback(self.on_controlunit_color_change)
                except KeyError:
                    pass

            self.view.Layout()

        with threading.Lock():
            wx.CallAfter(execute)

    def on_controlunit_measurement_change(self, model, data):
        with threading.Lock():
            if model.get_selected():
                wx.CallAfter(lambda: self.update_graph(model, data))

    def on_controlunit_color_change(self, model, data):
        wx.CallAfter(lambda: self.update_graph(model, model.get_measurements()))

    def update_graph(self, model, measurements):
        color = model.get_color()
        if color == wx.NullColour:
            color = wx.BLACK

        timestamps = list(map(lambda x: x.timestamp, measurements))
        temperatures = list(map(lambda x: x.temperature, measurements))
        shutter_status = list(map(lambda x: x.shutter_status, measurements))
        light_intensity = list(map(lambda x: x.light_intensity, measurements))

        if not timestamps or len(timestamps) < 2:
            timestamps += [time.time() - 10, time.time() - 5]
            temperatures += [0, 0]
            shutter_status += [0, 0]
            light_intensity += [0, 0]
            self._mocked = True
        elif self._mocked:
            self.redraw_all_units()
            self._mocked = False
            return

        self.view.update_temperature_graph(model.get_id(), color, timestamps, temperatures)
        self.view.update_status_graph(model.get_id(), color, timestamps, shutter_status)
        self.view.update_light_graph(model.get_id(), color, timestamps, light_intensity)
