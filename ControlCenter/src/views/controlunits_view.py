from src import mvc
from src.views.controlunit_view import ControlUnitView


class ControlUnitsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)

        self.SetBackgroundColour((0, 255, 0))

    def render_controlunit(self, controlunit_view):
        # render controlunit_view
        pass
