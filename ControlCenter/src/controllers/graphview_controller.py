import datetime

from src import mvc
from src.views.graphtab_view import GraphTabView


class GraphViewController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.controlunit_manager = controlunit_manager

        self.view = GraphTabView(view_parent)

        self.controlunit_manager.units.add_callback(self.on_controlunits_change)
        self.units = []

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.selected.add_callback(self.on_controlunit_selected_change)

    def on_controlunit_selected_change(self, model, selected):
        if selected:
            model.measurements.add_callback(self.on_controlunit_measurement_change)
            model.color.add_callback(self.on_controlunit_color_change)
        else:
            model.measurements.del_callback(self.on_controlunit_measurement_change)
            model.color.del_callback(self.on_controlunit_color_change)
            self.view.clear_trace(model.get_id())

    def on_controlunit_measurement_change(self, model, data):
        print("on measurement change")

        data = data.copy()  # copy otherwise we get RuntimeError if new measurements are added during iteration

        timestamps = list(map(lambda x: x.timestamp, data))
        temperatures = list(map(lambda x: x.temperature, data))
        self.view.update_temperature_graph(model.get_id(), model.get_name(), model.get_color(), timestamps, temperatures)

        # timestamps = []
        # temps = []
        # status = []
        # light = []
        #
        # for measurement in data:
        #     timestamps.append(int(measurement.timestamp))
        #     temps.append(measurement.temperature)
        #     status.append(measurement.shutter_status)
        #     light.append(measurement.light_intensity)
        #
        # _unit = None
        # found = False
        #
        # for unit in self.units:
        #     if unit["id"] == model.get_id():
        #         for i in range(len(timestamps)):
        #             unit["selected"] = model.get_selected()
        #             unit["color"] = model.get_color()
        #             unit["timestamps"].append(timestamps[i])
        #             unit["temperatures"].append(temps[i])
        #             unit["shutter_status"].append(status[i])
        #             unit["light_intensity"].append(light[i])
        #             found = True
        #
        # if not found:
        #     _unit={
        #         "id":model.get_id(),
        #         "selected":model.get_selected(),
        #         "color":model.get_color(),
        #         "timestamps":timestamps,
        #         "temperatures":temps,
        #         "shutter_status":status,
        #         "light_intensity":light
        #     }
        #     self.units.append(_unit)
        #
        # self.view.update_graphs(self.units)

    def on_controlunit_color_change(self, model, data):
        pass

