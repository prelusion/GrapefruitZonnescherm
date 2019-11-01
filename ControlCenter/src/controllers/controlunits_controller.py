import wx
import random
from src import mvc
from src.views.controlunits_view import ControlUnitsView
from src.views.controlunit_view import ControlUnitView


tmp = []
unit_colors = [
    (255, 0, 0),
    (255, 123, 0),
    (87, 6, 253),
    (1, 209, 126),
    (255, 33, 55),
    (21, 130, 10),
    (8, 16, 230),
]


def randcolor():
    global tmp, unit_colors
    result = random.choice(unit_colors)
    tmp.append(result)
    unit_colors.remove(result)
    if len(unit_colors) == 0:
        unit_colors = tmp.copy()
        tmp = []
    return result


class ControlUnitsController(mvc.Controller):
    def __init__(self, view_parent, controlunits_manager):
        super().__init__()

        self.controlunits_manager = controlunits_manager
        self.view = ControlUnitsView(view_parent)
        self.controlunit_views = []
        self.prevstate = {}

        for unit in self.controlunits_manager.get_units():
            comm, model = unit
            view = ControlUnitView(self.view)
            self.controlunit_views[model.get_id()] = view
            self.view.render_unit(model.get_id(), view)

        self.controlunits_manager.units.add_callback(self.on_units_changed)

    def on_units_changed(self, model, data):
        down_units = {k: self.prevstate[k] for k in set(self.prevstate) - set(data)}
        new_units = {k: data[k] for k in set(data) - set(self.prevstate)}

        for port, unit in down_units.items():
            comm, model = unit
            wx.CallAfter(lambda: self.view.remove_unit(model.get_id()))

        for port, unit in new_units.items():
            comm, model = unit
            wx.CallAfter(lambda: self.create_control_unit_view(model))

        self.prevstate = data.copy()

    def create_control_unit_view(self, model):
        view = ControlUnitView(self.view)
        view.set_connection(model.get_online())
        view.set_name(model.get_id())
        view.set_mode(model.get_mode())
        view.set_shutter_status(model.get_shutter_status())
        view.set_device_color(randcolor())
        view.set_temperature(model.get_temperature())

        model.name.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_name(value)))
        model.temperature.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_temperature(value)))
        model.shutter_status.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_shutter_status(value)))
        model.online.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_connection(value)))
        model.color.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_device_color(value)))
        model.mode.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_mode(value)))

        self.view.render_unit(model.get_id(), view)
