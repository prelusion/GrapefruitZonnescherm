import wx

from src import mvc
from src.views.controlunits_view import ControlUnitsView


class ControlUnitsController(mvc.Controller):
    def __init__(self, view_parent, controlunits_manager):
        super().__init__()

        self.controlunits_manager = controlunits_manager

        self.view = ControlUnitsView(view_parent)

        for unit in self.controlunits_manager.get_units():
            comm, model = unit
            self.view.render_unit(model.id, None)

        self.controlunits_manager.units.add_callback(self.on_units_changed)

    def on_units_changed(self, prevstate, newstate):
        down_units = {k: prevstate[k] for k in set(prevstate) - set(newstate)}
        new_units = {k: newstate[k] for k in set(newstate) - set(prevstate)}

        for port, unit in down_units.items():
            comm, model = unit
            wx.CallAfter(lambda: self.view.remove_unit(model.get_id()))

        for port, unit in new_units.items():
            comm, model = unit
            wx.CallAfter(lambda: self.view.render_unit(model.get_id(), None))
