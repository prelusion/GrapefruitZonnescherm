import wx

from src import mvc
from src.controllers.graphview_controller import GraphViewController
from src.views.manualcontrol_view import ManualControlView
from src.views.settings_view import SettingsView


class RightpanelDataController(mvc.Controller):
    def __init__(self, view_parent, filter_model, controlunit_manager, tabstate_model):
        super().__init__()

        self.view_parent = view_parent
        self.filter_model = filter_model
        self.controlunit_manager = controlunit_manager
        self.tabstate_model = tabstate_model
        self.current_view = None

        self.view = wx.Panel(view_parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.view.SetSizer(self.main_sizer)

        self.tabstate_model.state.add_callback(self.on_tab_change)

        self.graphview_controller = GraphViewController(self.view_parent, self.filter_model, self.controlunit_manager)
        self.manualcontrol_view = ManualControlView(self.view_parent)
        self.settings_view = SettingsView(self.view_parent)

        self.graphview_controller.view.Hide()
        self.manualcontrol_view.Hide()
        self.settings_view.Hide()

        self.main_sizer.Add(self.graphview_controller.view, wx.ID_ANY, wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.manualcontrol_view, wx.ID_ANY, wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.settings_view, wx.ID_ANY, wx.EXPAND | wx.ALL)

        self.show_graph()

    def on_tab_change(self, model, data):
        distributor = {
            model.View.settings: self.show_settings,
            model.View.graph: self.show_graph,
            model.View.manualcontrol: self.show_manual_control,
        }
        distributor[data]()

    def _show_view(self, view):
        if self.current_view:
            self.current_view.Hide()
        self.current_view = view
        self.current_view.Show()
        self.main_sizer.Layout()

    def show_settings(self):
        self._show_view(self.settings_view)

    def show_graph(self):
        self._show_view(self.graphview_controller.view)

    def show_manual_control(self):
        self._show_view(self.manualcontrol_view)
