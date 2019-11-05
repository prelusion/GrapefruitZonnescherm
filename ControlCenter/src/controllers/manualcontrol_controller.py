from src import mvc
from src.views.manualcontrol_view import ManualControlView


class ManualControlController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.view = ManualControlView(view_parent)
