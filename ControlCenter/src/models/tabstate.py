from src import mvc
from enum import Enum, auto


class TabstateModel(mvc.Model):

    class View(Enum):
        manualcontrol = auto()
        graph = auto()
        settings = auto()

    def __init__(self):
        self.state = mvc.Observable(self, None)
        self.set_manualcontrol_view()

    def set_manualcontrol_view(self):
        self.state.set(self.View.manualcontrol)

    def set_graph_view(self):
        self.state.set(self.View.graph)

    def set_settings_view(self):
        self.state.set(self.View.settings)
