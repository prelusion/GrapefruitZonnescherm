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

        self._unit_changing = False

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.selected.add_callback(self.on_controlunit_selected_change)

    def redraw_all_units(self):
        for unit in self.controlunit_manager.get_selected_units():
            comm, model = unit
            self.update_graph(model, model.get_measurements())

    def on_controlunit_selected_change(self, model, selected):
        with threading.Lock():
            logger.info("[THREADING] enter lock")
            if not selected:
                self.view.remove_device(model.get_id())
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
            # wx.CallAfter(model.done_selecting)
            wx.CallAfter(self.view.Layout)
        logger.info("[THREADING] exit lock")

    def on_controlunit_measurement_change(self, model, data):
        with threading.Lock():
            logger.info("[THREADING] enter lock")
            if model.get_selected():
                wx.CallAfter(lambda: self.update_graph(model, data))

        logger.info("[THREADING] exit lock")

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
        if not temperatures or len(temperatures) < 2:
            temperatures += [0, 0]
        if not shutter_status or len(shutter_status) < 2:
            shutter_status += [0, 0]
        if not light_intensity or len(light_intensity) < 2:
            light_intensity += [0, 0]

        self.view.update_temperature_graph(model.get_id(), color, timestamps, temperatures)
        self.view.update_status_graph(model.get_id(), color, timestamps, shutter_status)
        self.view.update_light_graph(model.get_id(), color, timestamps, light_intensity)
