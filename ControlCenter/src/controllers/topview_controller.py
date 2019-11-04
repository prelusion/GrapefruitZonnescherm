from src import mvc
from src.views.top_view import TopView


class TopViewController(mvc.Controller):
    def __init__(self, view_parent, tabstate_model):
        super().__init__()

        self.view = TopView(view_parent)
        self.view.tab_view_controller.set_tabstate_model(tabstate_model)
