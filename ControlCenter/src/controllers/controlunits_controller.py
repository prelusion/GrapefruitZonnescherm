from src import mvc
from src.views.controlunits_view import ControlUnitsView
from src.views.controlunit_view import ControlUnitView


class ControlUnitsController(mvc.Controller):
    def __init__(self, parent, controlunits_manager):
        super().__init__()

        self.units = {}

        self.controlunits_manager = controlunits_manager

        self.set_view(ControlUnitsView(parent))

        for unit in self.controlunits_manager.get_units():
            comm, model = unit

            unit_view = ControlUnitView(self.get_view())

            self.units[model.id] = unit_view

            self.get_view().render_unit(unit_view)
