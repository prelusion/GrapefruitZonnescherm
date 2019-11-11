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
            print("rendering unit in init")
            self.create_control_unit_view(model)

        self.controlunits_manager.units.add_callback(self.on_units_changed)

        debug = False
        if debug:
            for i in range(3):
                view = ControlUnitView(view_parent)
                self.view.render_unit(1, view)

    def on_units_changed(self, model, data):
        down_units = [i for i in set(self.prevstate) - set(data)]
        new_units = [i for i in set(data) - set(self.prevstate)]
        print("new units:", new_units)
        print("down units:", down_units)
        #
        # for comm, model in down_units:
        #     wx.CallAfter(lambda: self.view.remove_unit(model.get_id()))
        #
        # for comm, model in new_units:
        #     wx.CallAfter(lambda: self.create_control_unit_view(model))
        #
        # self.prevstate = data.copy()

    def create_control_unit_view(self, model):
        print("CREATE CONTROL UNIT VIEW")
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
        model.online.add_callback(lambda model, value: wx.CallAfter(lambda: self.on_unit_online_change(model, value, view)))
        model.color.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_device_color(value)))
        model.manual.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_manual(value)))
        model.selected.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_selected(value)))

        view.set_on_click_callback(lambda e: self.on_unit_click(model, view))
        self.view.render_unit(model.get_id(), view)

        if not model.get_initialized():
            wx.MessageBox("Please select your new device and go to the settings tab",
                          'New device detected',
                          wx.OK | wx.ICON_INFORMATION)

    def on_unit_click(self, model, view):
        # if model.is_selecting():
        #     return
        
        view.set_selected(True) if not model.get_selected() else view.set_selected(False)
        model.set_selected(not model.get_selected())

    def on_unit_online_change(self, model, value, view):
        print("on unit online change", value)
        view.set_connection(value)
        # print("view", view.IsEnabled())
        # print("view", view)
        # print("enabled", view.IsEnabled())
        # if value:
        #     view.Enable()
        # else:
        #     view.Disable()
        # print("enabled", view.IsEnabled())

        view.Enable()

        view.Layout()
        view.Refresh()
        view.Update()
        # self.view.Layout()
        # self.view.Refresh()
        # self.view.Update()
