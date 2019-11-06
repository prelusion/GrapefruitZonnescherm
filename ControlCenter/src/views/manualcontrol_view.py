import wx

from src import mvc
from src import widgets


class ManualControlView(mvc.View):
    COLOR_ERROR = wx.RED
    COLOR_INFO = wx.BLACK

    def __init__(self, parent):
        super().__init__(parent)

        self.callbacks = {}

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)
        self.main_sizer.AddSpacer(50)

        self.inner_panel = wx.Panel(self)
        self.main_sizer.Add(self.inner_panel, 20, wx.CENTER)

        grid_sizer = wx.GridSizer(14, 3, 0, 20)
        self.inner_panel.SetSizer(grid_sizer)

        # Manual toggle
        self.device_name = widgets.CenteredLabel(self.inner_panel, label="Manual Control", horizontal=False)
        grid_sizer.Add(self.device_name, flag=wx.EXPAND | wx.ALL)

        self.toggle_on = wx.ToggleButton(self.inner_panel, id=wx.ID_ANY, label="ON", name="on")
        grid_sizer.Add(self.toggle_on, flag=wx.EXPAND | wx.ALL)

        self.toggle_off = wx.ToggleButton(self.inner_panel, id=wx.ID_ANY, label="OFF", name="off")
        grid_sizer.Add(self.toggle_off, flag=wx.EXPAND | wx.ALL)

        self.toggle_on.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_manual_control)
        self.toggle_off.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_manual_control)

        # Shutter control
        self.device_name = widgets.CenteredLabel(self.inner_panel, label="Shutter Control", horizontal=False)
        grid_sizer.Add(self.device_name, flag=wx.EXPAND | wx.ALL)

        self.toggle_down = wx.ToggleButton(self.inner_panel, id=wx.ID_ANY, label="DOWN", name="down")
        grid_sizer.Add(self.toggle_down, flag=wx.EXPAND | wx.ALL)

        self.toggle_up = wx.ToggleButton(self.inner_panel, id=wx.ID_ANY, label="UP", name="up")
        grid_sizer.Add(self.toggle_up, flag=wx.EXPAND | wx.ALL)

        self.toggle_down.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_shutter)
        self.toggle_up.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_shutter)

        self.toggle_off.SetValue(1)
        self.disable_manual_control_buttons()

    def on_toggle_shutter(self, event):
        e = event.GetEventObject()

        if e.GetName() == "down":
            if e.GetValue():
                self.toggle_up.SetValue(0)
                cb = self.callbacks["toggle-down"]
                if cb: cb()
            else:
                self.toggle_down.SetValue(1)
        if e.GetName() == "up":
            if e.GetValue():
                self.toggle_down.SetValue(0)
                cb = self.callbacks["toggle-up"]
                if cb: cb()
            else:
                self.toggle_up.SetValue(1)

    def on_toggle_manual_control(self, event):
        e = event.GetEventObject()

        if e.GetName() == "on":
            if e.GetValue():
                self.toggle_off.SetValue(0)
                self.enable_manual_control_buttons()
                cb = self.callbacks["enable-manual-control"]
                if cb: cb()
            else:
                self.toggle_on.SetValue(1)
        if e.GetName() == "off":
            if e.GetValue():
                self.toggle_on.SetValue(0)
                self.disable_manual_control_buttons()
                cb = self.callbacks["disable-manual-control"]
                if cb: cb()
                self.toggle_off.SetValue(1)
            else:
                self.toggle_off.SetValue(1)

    def enable_manual_control_buttons(self):
        self.toggle_down.Enable()
        self.toggle_up.Enable()

    def disable_manual_control_buttons(self):
        self.toggle_down.Disable()
        self.toggle_up.Disable()
        self.toggle_down.SetValue(0)
        self.toggle_up.SetValue(0)

    def set_enable_manual_control_callback(self, callback):
        self.callbacks["enable-manual-control"] = callback

    def set_disable_manual_control_callback(self, callback):
        self.callbacks["disable-manual-control"] = callback

    def set_toggle_up_callback(self, callback):
        self.callbacks["toggle-up"] = callback

    def set_toggle_down_callback(self, callback):
        self.callbacks["toggle-down"] = callback

    def disable_manual_control(self):
        self.toggle_down.Disable()
        self.toggle_up.Disable()
        self.toggle_on.Disable()
        self.toggle_off.Disable()

    def enable_manual_control(self):
        self.toggle_on.Enable()
        self.toggle_off.Enable()

    def set_manual_enabled(self, boolean):
        if boolean:
            self.toggle_on.SetValue(1)
            self.toggle_off.SetValue(0)
            self.enable_manual_control_buttons()
        else:
            self.toggle_on.SetValue(0)
            self.toggle_off.SetValue(1)
            self.disable_manual_control_buttons()

    def show_error(self, message):
        print("show dialog")
        wx.MessageBox(message, 'Error',
                      wx.OK | wx.ICON_ERROR)
