import wx

from src import mvc
from src.views.controlunit_view import ControlUnitView
from src.views.controlunits_view import ControlUnitsView


class ControlUnitsController(mvc.Controller):
    def __init__(self, view_parent, controlunits_manager):
        super().__init__()

        self.controlunits_manager = controlunits_manager
        self.view = ControlUnitsView(view_parent)
        self.controlunit_views = []
        self.prevstate = []

        units = self.controlunits_manager.get_units()
        for unit in units:
            self.create_control_unit_view(unit.model)
            self.prevstate = units.copy()

        self.controlunits_manager.units.add_callback(self.on_units_changed)

    def on_units_changed(self, model, data):
        down_units = [i for i in set(self.prevstate) - set(data)]
        new_units = [i for i in set(data) - set(self.prevstate)]

        for unit in down_units:
            wx.CallAfter(lambda: self.view.remove_unit(unit.model.get_id()))

        for unit in new_units:
            wx.CallAfter(lambda: self.create_control_unit_view(unit.model))

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
        model.online.add_callback(
            lambda model, value: wx.CallAfter(lambda: self.on_unit_online_change(model, value, view)))
        model.color.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_device_color(value)))
        model.manual.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_manual(value)))
        model.selected.add_callback(lambda model, value: wx.CallAfter(lambda: view.set_selected(value)))
        view.set_on_click_callback(lambda e: self.on_unit_click(model, view))

        if model.get_online(): view.Enable()

        self.view.render_unit(model.get_id(), view)

        if not model.get_initialized():
            wx.MessageBox("Please select your new device and go to the settings tab",
                          'New device detected',
                          wx.OK | wx.ICON_INFORMATION)

    def on_unit_click(self, model, view):
        units = self.controlunits_manager.get_selected_units()

        if len(units) >= 2 and not model.get_selected():
            wx.CallAfter(lambda: self.view.show_error("You can only select two control units at a time",
                                                      title="Can not select more units"))
            return

        view.set_selected(True) if not model.get_selected() else view.set_selected(False)
        model.set_selected(not model.get_selected())

    @staticmethod
    def on_unit_online_change(model, online: bool, view):
        view.set_connection(online)
        view.Layout()
        view.Refresh()
        view.Update()
