from src import mvc


class FilterView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((255, 50, 0))
