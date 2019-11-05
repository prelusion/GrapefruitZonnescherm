from src import mvc
from src.views.manualcontrol_view import ManualControlView


class ManualControlController(mvc.Controller):
    def __init__(self, view_parent, controlunit_manager):
        super().__init__()

        self.controlunit_manager = controlunit_manager

        self.view = ManualControlView(view_parent)

        self.view.set_enable_manual_control_callback(self.on_manual_control_enable)
        self.view.set_disable_manual_control_callback(self.on_manual_control_disable)
        self.view.set_toggle_up_callback(self.on_toggle_up)
        self.view.set_toggle_down_callback(self.on_toggle_down)

    def on_manual_control_enable(self):
        print("manual enable")
        for comm, model in self.controlunit_manager.get_selected_units():
            print("enabling for unit..")
            if comm.set_manual(True):
                print("unit is now in manual mode")
                print("reading manual mode:", comm.get_manual())

    def on_manual_control_disable(self):
        print("manual disable")

    def on_toggle_up(self):
        print("toggle up")

    def on_toggle_down(self):
        print("toggle down")
