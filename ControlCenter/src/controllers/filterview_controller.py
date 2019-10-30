import wx

from src import mvc
from src.views.filter_view import FilterView


class FilterViewController(mvc.Controller):
    def __init__(self, view_parent, filter_model):
        super().__init__()

        self.filter_model = filter_model

        self.view = FilterView(view_parent)

