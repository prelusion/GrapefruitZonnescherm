from src import mvc


class GraphView(mvc.View):

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((119, 119, 122))