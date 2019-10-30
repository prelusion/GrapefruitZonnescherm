from src import mvc


class ControlUnitsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((0, 255, 0))
