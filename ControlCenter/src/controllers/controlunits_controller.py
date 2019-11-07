import random

import wx

from src import mvc
from src.views.controlunit_view import ControlUnitView
from src.views.controlunits_view import ControlUnitsView

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

        for comm, model in self.controlunits_manager.get_units():
            view = ControlUnitView(self.view)
            self.controlunit_views[model.get_id()] = view
            self.view.render_unit(model.get_id(), view)

        self.controlunits_manager.units.add_callback(self.on_units_changed)

        debug = False
        if debug:
            for i in range(3):
                view = ControlUnitView(view_parent)
                self.view.render_unit(1, view)

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
        view.set_name(model.get_name())
        view.set_manual(model.get_manual())
        view.set_shutter_status(model.get_shutter_status())
        view.set_device_color(model.get_color())
        view.set_temperature(model.get_temperature())
        view.set_selected(model.get_selected())

        model.name.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_name(value)))
        model.temperature.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_temperature(value)))
        model.shutter_status.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_shutter_status(value)))
        model.online.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_connection(value)))
        # model.color.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_device_color(value)))
        model.manual.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_manual(value)))
        model.selected.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_selected(value)))

        view.set_on_click_callback(lambda e: self.on_unit_click(model, view))
        self.view.render_unit(model.get_id(), view)

        if not model.get_initialized():
            wx.MessageBox("Please select your new device and go to the settings tab",
                          'New device detected',
                          wx.OK | wx. ICON_INFORMATION)

    def on_unit_click(self, model, view):
        view.set_selected(True) if not model.get_selected() else view.set_selected(False)
        model.set_selected(not model.get_selected())
