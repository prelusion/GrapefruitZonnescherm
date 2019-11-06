import wx

from src import mvc
from src.controllers.graphview_controller import GraphViewController
from src.controllers.settingsview_controller import SettingsViewController
from src.controllers.manualcontrol_controller import ManualControlController


class RightpanelDataController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager, tabstate_model):
        super().__init__()

        self.view_parent = view_parent
        self.controlunit_manager = controlunit_manager
        self.tabstate_model = tabstate_model
        self.current_view = None

        self.view = wx.Panel(view_parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.view.SetSizer(self.main_sizer)

        self.tabstate_model.state.add_callback(self.on_tab_change)

        self.graphview_controller = GraphViewController(self.view, self.controlunit_manager)
        self.manualcontrolview_controller = ManualControlController(self.view, self.controlunit_manager)
        self.settingsview_controller = SettingsViewController(self.view, controlunit_manager)

        self.graphview_controller.view.Hide()
        self.manualcontrolview_controller.view.Hide()
        self.settingsview_controller.view.Hide()

        self.main_sizer.Add(self.graphview_controller.view, wx.ID_ANY, wx.EXPAND | wx.ALL)
        self.main_sizer.Add(self.manualcontrolview_controller.view, wx.ID_ANY, wx.EXPAND | wx.ALL, 10)
        self.main_sizer.Add(self.settingsview_controller.view, wx.ID_ANY, wx.EXPAND | wx.ALL)

        self.show_graph()
        self.show_manual_control()

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
        self._show_view(self.settingsview_controller.view)

    def show_graph(self):
        self._show_view(self.graphview_controller.view)

    def show_manual_control(self):
        self._show_view(self.manualcontrolview_controller.view)
