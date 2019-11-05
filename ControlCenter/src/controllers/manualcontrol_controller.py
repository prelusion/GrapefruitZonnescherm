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

        if not self.controlunit_manager.get_selected_units():
            self.view.set_selected_devices_none()

        self.controlunit_manager.units.add_callback(self.on_units_change)

    def on_units_change(self, model, data):
        for comm, model in self.controlunit_manager.get_units():
            model.selected.add_callback(self.on_unit_selected_change)

    def on_unit_selected_change(self, model, data):
        if self.controlunit_manager.get_selected_units():
            self.view.set_selected_devices_not_none()
        else:
            self.view.set_selected_devices_none()

    def on_manual_control_enable(self):
        for comm, model in self.controlunit_manager.get_selected_units():
            if comm.set_manual(True):
                model.set_manual(True)

    def on_manual_control_disable(self):
        for comm, model in self.controlunit_manager.get_selected_units():
            if comm.set_manual(False):
                model.set_manual(False)

    def on_toggle_up(self):
        print("toggle up")

    def on_toggle_down(self):
        print("toggle down")
