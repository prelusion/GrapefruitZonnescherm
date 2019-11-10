import logging
import os
import threading

import wx

from src import const
from src import controlunit
from src import db
from src import util
from src.controllers.controlunits_controller import ControlUnitsController
from src.controllers.filterview_controller import FilterViewController
from src.controllers.rightpaneldata_controller import RightpanelDataController
from src.controllers.topview_controller import TopViewController
from src.models.controlunit_manager import ControlUnitManager
from src.models.tabstate import TabstateModel

logger = logging.getLogger(__name__)


class App(wx.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app_id = None

        self.controlunit_manager = ControlUnitManager()
        self.tabstate_model = TabstateModel()

        self.init()
        self.start_background_services()

    def init(self):
        if not os.path.exists(const.DATA_DIR):
            os.makedirs(const.DATA_DIR)

        db.init()
        logger.info(f"current control units in database: {db.select_all(db.TABLE_CONTROL_UNITS)}")
        # logger.info(f"current measurements in database: {db.select_all(db.TABLE_MEASUREMENTS)}")

        app_data = util.load_json_from_file(const.APP_DATA_FILE)

        if "id" not in app_data:
            app_data["id"] = util.generate_16bit_int()
            util.save_json_to_file(const.APP_DATA_FILE, app_data)

        self.app_id = app_data["id"]

    def start_background_services(self):
        t = threading.Thread(target=controlunit.online_control_unit_service,
                             args=(self.app_id, self.controlunit_manager,), daemon=True)
        t.start()

        t = threading.Thread(target=controlunit.sensor_data_service,
                             args=(self.controlunit_manager, 15), daemon=True)
        t.start()


class MainView(wx.Frame):
    def __init__(self, app, title):
        super().__init__(None, title=title, size=(1500, 800))

        self.SetMinSize((1450, 750))
        self.app = app
        self.SetIcon(wx.Icon(os.path.join(const.ROOT_DIR, "Assets", "Icons", "logo.ico")))
        self.Center()

        # Main panel
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)

        # Top bar
        toppanel_controller = TopViewController(main_panel, self.app.tabstate_model)
        main_sizer.Add(toppanel_controller.view, 1, wx.EXPAND | wx.ALL)

        # Center panel
        center_panel = wx.Panel(main_panel)
        center_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        center_panel.SetSizer(center_panel_sizer)
        main_sizer.Add(center_panel, 15, wx.EXPAND | wx.ALL)

        # Left panel
        left_panel = wx.Panel(center_panel)
        left_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        left_panel.SetSizer(left_panel_sizer_vbox)

        # Right panel
        right_panel = wx.Panel(center_panel)
        right_panel_sizer_vbox = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(right_panel_sizer_vbox)

        # Left panel components
        controlunits_controller = ControlUnitsController(left_panel, self.app.controlunit_manager)
        filterview_controller = FilterViewController(left_panel, self.app.controlunit_manager)
        left_panel_sizer_vbox.Add(controlunits_controller.view, 8, wx.EXPAND | wx.ALL)
        left_panel_sizer_vbox.Add(filterview_controller.view, 1, wx.EXPAND | wx.ALL)
        center_panel_sizer.Add(left_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        # Right panel components
        rightpanel_controller = RightpanelDataController(self.app, right_panel,
                                                         self.app.controlunit_manager,
                                                         self.app.tabstate_model)
        right_panel_sizer_vbox.Add(rightpanel_controller.view, 10, wx.EXPAND | wx.ALL)
        center_panel_sizer.Add(right_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)


def mainloop():
    app = App(False)
    mainview = MainView(app, "Grapefruit Control Center")
    mainview.Show()
    app.MainLoop()


if __name__ == "__main__":
    mainloop()
