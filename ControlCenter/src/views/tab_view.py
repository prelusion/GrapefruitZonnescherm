from src import mvc


class TabView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((255, 100, 75))
