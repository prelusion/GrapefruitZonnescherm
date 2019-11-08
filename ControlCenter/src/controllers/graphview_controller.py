import logging
import threading

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
            else:
                try:
                    model.measurements.del_callback(self.on_controlunit_measurement_change)
                except KeyError as e:
                    logger.exception(e)
            # wx.CallAfter(model.done_selecting)
            wx.CallAfter(self.view.Layout)
        logger.info("[THREADING] exit lock")

    def on_controlunit_measurement_change(self, model, data):
        with threading.Lock():
            logger.info("[THREADING] enter lock")
            if model.get_selected():
                wx.CallAfter(lambda: self.update_graph(model, data))

        logger.info("[THREADING] exit lock")

    def update_graph(self, model, measurements):
        timestamps = list(map(lambda x: x.timestamp, measurements))
        temperatures = list(map(lambda x: x.temperature, measurements))
        shutter_status = list(map(lambda x: x.shutter_status, measurements))
        light_intensity = list(map(lambda x: x.light_intensity, measurements))

        if not temperatures:
            temperatures.append(0)
            temperatures.append(0)
        if not shutter_status:
            shutter_status.append(0)
            shutter_status.append(0)
        if not light_intensity:
            light_intensity.append(0)
            light_intensity.append(0)

        self.view.update_temperature_graph(model.get_id(),
                                           model.get_color(),
                                           timestamps,
                                           temperatures)

        self.view.update_status_graph(model.get_id(),
                                      model.get_color(),
                                      timestamps,
                                      shutter_status)

        self.view.update_light_graph(model.get_id(),
                                     model.get_color(),
                                     timestamps,
                                     light_intensity)
