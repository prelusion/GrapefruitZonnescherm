import datetime

from src import mvc
from src.views.graphtab_view import GraphTabView


class GraphViewController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.controlunit_manager = controlunit_manager

        # self.graphs_view = src.views.tab_data_view.GraphView(view_parent)
        self.view = GraphTabView(view_parent)

        self.controlunit_manager.units.add_callback(self.on_controlunits_change)
        self.units = []

    def on_controlunits_change(self, model, data):
        for port, unit in data.items():
            comm, model = unit
            model.measurements.add_callback(self.on_controlunit_measurement_change)
            model.color.add_callback(self.on_controlunit_color_change)
            model.selected.add_callback(self.on_controlunit_selected_change)

    def on_controlunit_measurement_change(self, model, data):
        timestamps = []
        temps = []
        status = []
        light = []

        for measurement in data:
            #timestamps.append(int(datetime.datetime.timestamp(datetime.datetime.now())))
            timestamps.append(int(measurement.timestamp))
            temps.append(measurement.temperature)
            status.append(measurement.shutter_status)
            light.append(measurement.light_intensity)

        _unit = None

        for unit in self.units:
            if unit["id"] == model.get_id():
                for i in range(len(timestamps)):
                    unit["selected"] = model.get_selected()
                    unit["color"] = model.get_color()
                    unit["timestamps"].append(timestamps[i])
                    unit["temperatures"].append(temps[i])
                    unit["shutter_status"].append(status[i])
                    unit["light_intensity"].append(light[i])
        if _unit is None:
            _unit={
                "id":model.get_id(),
                "selected":model.get_selected(),
                "color":model.get_color(),
                "timestamps":timestamps,
                "temperatures":temps,
                "shutter_status":status,
                "light_intensity":light
            }
            self.units.append(_unit)

        self.view.update_graphs(self.units)

    def on_controlunit_color_change(self, model, data):
        pass

    def on_controlunit_selected_change(self, model, data):
        pass
        # print("Model with id:", model.get_id(), "selected:", data)
