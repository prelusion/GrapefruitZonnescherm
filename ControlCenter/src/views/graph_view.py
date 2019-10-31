from src import mvc


class GraphView(mvc.View):

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((0, 200, 80))

    def set_measurements(self, unit_id, measurements):
        pass

    def set_color(self, unit_id, color):
        pass
