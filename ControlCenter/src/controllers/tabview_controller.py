import wx

from src import mvc
from src.views.tab_view import TabView


class TabviewController(mvc.Controller):
    def __init__(self, view_parent):
        super().__init__()

        self.tabstate_model = None

        self.view = TabView(view_parent)
        self.view.graph_tab.Bind(wx.EVT_BUTTON, self.on_show_graph_btn)
        self.view.manual_tab.Bind(wx.EVT_BUTTON, self.on_show_manual_control_btn)
        self.view.settings_tab.Bind(wx.EVT_BUTTON, self.on_show_settings_btn)

    def set_tabstate_model(self, tabstate_model):
        self.tabstate_model = tabstate_model

    def on_show_graph_btn(self, e):
        self.tabstate_model.set_graph_view()

    def on_show_manual_control_btn(self, e):
        self.tabstate_model.set_manualcontrol_view()

    def on_show_settings_btn(self, e):
        self.tabstate_model.set_settings_view()
