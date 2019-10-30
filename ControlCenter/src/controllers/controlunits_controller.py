import wx

from src import mvc
from src.views.controlunit_view import ControlUnitView
from src.views.controlunits_view import ControlUnitsView


class ControlUnitsController(mvc.Controller):
    def __init__(self, parent, controlunits_manager):
        super().__init__()

        self.controlunits_manager = controlunits_manager

        self.set_view(ControlUnitsView(parent))

        for unit in self.controlunits_manager.get_units():
            comm, model = unit

            unit_view = ControlUnitView(self.get_view())

            self.get_view().render_unit(model.id, unit_view)

        self.controlunits_manager.units.add_callback(self.on_units_changed)

    def on_units_changed(self, prevstate, state):
        # print("ON UNITS CHANGED:")
        # print("prev:", prevstate)
        # print("new: ", state)
        down_units = {k: prevstate[k] for k in set(prevstate) - set(state)}
        new_units = {k: state[k] for k in set(state) - set(prevstate)}
        print("down:", down_units)
        print("new:", new_units)
        for port, unit in down_units.items():
            comm, model = unit
            wx.CallAfter(lambda: self.get_view().remove_unit(model.get_id()))

        for port, unit in new_units.items():
            comm, model = unit
            unit_view = ControlUnitView(self.get_view())
            wx.CallAfter(lambda: self.get_view().render_unit(model.get_id(), unit_view))
