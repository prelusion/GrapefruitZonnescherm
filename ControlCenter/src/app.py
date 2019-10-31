import os
import threading
import json
import wx

from src import const
from src import controlunit
from src.controllers.controlunits_controller import ControlUnitsController
from src.controllers.filterview_controller import FilterViewController
from src.controllers.graphview_controller import GraphViewController
from src.models.controlunit_manager import ControlUnitManager
from src.models.filter import FilterModel
from src.views.tab_view import TabView

from src import util


class App(wx.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app_id = None

        self.controlunit_manager = ControlUnitManager()
        self.filter_model = FilterModel()

        self.init()
        self.start_background_services()

    def init(self):
        if not os.path.exists(const.DATA_DIR):
            os.makedirs(const.DATA_DIR)

        app_data = util.load_json_from_file(const.APP_DATA_FILE)

        if "id" not in app_data:
            app_data["id"] = util.generate_16bit_int()
            util.save_json_to_file(const.APP_DATA_FILE, app_data)

        self.app_id = app_data["id"]

        print(self.app_id)

    def start_background_services(self):
        t = threading.Thread(target=controlunit.online_control_unit_service,
                             args=(self.controlunit_manager,), daemon=True)
        t.start()


class MainView(wx.Frame):
    def __init__(self, app, title):
        super().__init__(None, title=title, size=(1200, 700))

        self.app = app
        self.SetIcon(wx.Icon(os.path.join(const.ROOT_DIR, "Assets", "Icons", "logo.ico")))

        # Init main panel
        main_panel = wx.Panel(self)
        main_sizer_hbox = wx.BoxSizer(wx.HORIZONTAL)
        main_panel.SetSizer(main_sizer_hbox)

        # Init left panel
        left_panel = wx.Panel(main_panel)
        left_panel.SetBackgroundColour((1, 1, 1))
        left_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        left_panel.SetSizer(left_panel_sizer_vbox)

        # Init right panel
        right_panel = wx.Panel(main_panel)
        right_panel.SetBackgroundColour((0, 0, 255))
        right_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(right_panel_sizer_vbox)

        # Left panel components
        controlunits_controller = ControlUnitsController(left_panel, self.app.controlunit_manager)
        filterview_controller = FilterViewController(left_panel, self.app.filter_model)
        left_panel_sizer_vbox.Add(controlunits_controller.view, 3, wx.EXPAND | wx.ALL)
        left_panel_sizer_vbox.Add(filterview_controller.view, 1, wx.EXPAND | wx.ALL)
        main_sizer_hbox.Add(left_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

        # Right panel components
        tab_view = TabView(right_panel)
        graphview_controller = GraphViewController(right_panel, self.app.filter_model, self.app.controlunit_manager)
        right_panel_sizer_vbox.Add(tab_view, 1, wx.EXPAND | wx.ALL)
        right_panel_sizer_vbox.Add(graphview_controller.view, 10, wx.EXPAND | wx.ALL)
        main_sizer_hbox.Add(right_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)


def mainloop():
    app = App(False)
    mainview = MainView(app, "Grapefruit controlpanel")
    mainview.Show()
    app.MainLoop()


if __name__ == "__main__":
    mainloop()
