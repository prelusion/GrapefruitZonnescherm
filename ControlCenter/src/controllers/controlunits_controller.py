import wx

from src import mvc
from src.views.controlunits_view import ControlUnitsView
from src.views.controlunit_view import ControlUnitView


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
            wx.CallAfter(lambda: self.view.render_unit(model.get_id(), ControlUnitView(self.view)))

        self.prevstate = data.copy()
