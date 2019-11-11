import wx

from src import mvc
from src import widgets
from src import util


class LabeledDoubleToggleButton(wx.Panel):
    STATE_TOGGLED = 1
    STATE_DEFAULT = 0

    def __init__(self, parent, label, button1_label, button2_label, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._button1_callback = None
        self._button2_callback = None

        self.label = widgets.CenteredLabel(parent, label=label, horizontal=False)
        self.label.SetFont(util.MainFont("normal"))


        self.button1 = wx.ToggleButton(parent, id=wx.ID_ANY, label=button1_label, name="1")
        self.button2 = wx.ToggleButton(parent, id=wx.ID_ANY, label=button2_label, name="2")

        self.button1.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_1)
        self.button2.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle_2)

    def set_button1_callback(self, callback):
        self._button1_callback = callback

    def set_button2_callback(self, callback):
        self._button2_callback = callback

    def on_toggle_1(self, e):
        self.button1.SetValue(self.STATE_DEFAULT)
        if self._button1_callback: self._button1_callback()

    def on_toggle_2(self, e):
        self.button2.SetValue(self.STATE_DEFAULT)
        if self._button2_callback: self._button2_callback()

    def on_toggle_1_success(self):
        self.button1.SetValue(self.STATE_DEFAULT)
        self.button2.SetValue(self.STATE_TOGGLED)

    def on_toggle_2_success(self):
        self.button1.SetValue(self.STATE_TOGGLED)
        self.button2.SetValue(self.STATE_DEFAULT)


class ManualControlView(mvc.View):
    COLOR_ERROR = wx.RED
    COLOR_INFO = wx.BLACK

    def __init__(self, parent):
        super().__init__(parent)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

        self.inner_panel = wx.Panel(self)
        self.main_sizer.Add(self.inner_panel, 20, wx.CENTER)

        grid_sizer = wx.GridSizer(14, 3, 0, 20)
        self.inner_panel.SetSizer(grid_sizer)

        # Top text
        grid_sizer.Add(wx.StaticText(self.inner_panel))
        manualText = wx.StaticText(self.inner_panel, label="Manual:")
        manualText.SetFont(util.MainFont("title", fontsize=12))
        grid_sizer.Add(manualText, wx.ALIGN_CENTER)
        grid_sizer.Add(wx.StaticText(self.inner_panel))

        # Selected unit name
        self.selected_text = wx.StaticText(self.inner_panel, label="Selected Unit: ")
        self.unit_name = wx.StaticText(self.inner_panel, label="No unit selected")
        self.unit_name.SetFont(util.MainFont("Normal", fontsize=14))
        grid_sizer.Add(self.selected_text, flag=wx.EXPAND | wx.ALL)
        grid_sizer.Add(self.unit_name, flag=wx.EXPAND | wx.ALL)
        grid_sizer.Add(wx.StaticText(self.inner_panel), flag=wx.EXPAND | wx.ALL)

        # Manual toggle
        self.manual_toggle = LabeledDoubleToggleButton(self.inner_panel, "Manual Control", "ON", "OFF")
        grid_sizer.Add(self.manual_toggle.label, flag=wx.EXPAND | wx.ALL)
        grid_sizer.Add(self.manual_toggle.button1, flag=wx.EXPAND | wx.ALL)
        grid_sizer.Add(self.manual_toggle.button2, flag=wx.EXPAND | wx.ALL)

        # Shutter control
        self.shutter_control = LabeledDoubleToggleButton(self.inner_panel, "Shutter Control", "DOWN", "UP")
        grid_sizer.Add(self.shutter_control.label, flag=wx.EXPAND | wx.ALL)
        grid_sizer.Add(self.shutter_control.button1, flag=wx.EXPAND | wx.ALL)
        grid_sizer.Add(self.shutter_control.button2, flag=wx.EXPAND | wx.ALL)

        self.disable_manual_control_buttons()
        self.disable_shutter_control_buttons()

    def set_enable_manual_control_callback(self, callback):
        self.manual_toggle.set_button1_callback(callback)

    def set_disable_manual_control_callback(self, callback):
        self.manual_toggle.set_button2_callback(callback)

    def set_toggle_up_callback(self, callback):
        self.shutter_control.set_button2_callback(callback)

    def set_toggle_down_callback(self, callback):
        self.shutter_control.set_button1_callback(callback)

    def enable_manual_control_buttons(self):
        self.manual_toggle.button1.Enable()
        self.manual_toggle.button2.Enable()

    def disable_manual_control_buttons(self):
        self.manual_toggle.button1.Disable()
        self.manual_toggle.button2.Disable()

    def enable_shutter_control_buttons(self):
        self.shutter_control.button1.Enable()
        self.shutter_control.button2.Enable()

    def disable_shutter_control_buttons(self):
        self.shutter_control.button1.Disable()
        self.shutter_control.button2.Disable()

    def enable_manual_control(self):
        self.enable_manual_control_buttons()

    def disable_manual_control(self):
        self.disable_manual_control_buttons()
        self.disable_shutter_control_buttons()

    def set_selected_unit_name(self, name = "No unit selected"):
        if not name: name = "uninitialized"
        self.unit_name.SetLabel(name)

    def toggle_manual_control(self, boolean):
        """
        :param boolean: True (on toggled) False (off toggled)
        """
        if boolean:
            self.manual_toggle.button1.SetValue(LabeledDoubleToggleButton.STATE_TOGGLED)
            self.manual_toggle.button2.SetValue(LabeledDoubleToggleButton.STATE_DEFAULT)
        else:
            self.manual_toggle.button1.SetValue(LabeledDoubleToggleButton.STATE_DEFAULT)
            self.manual_toggle.button2.SetValue(LabeledDoubleToggleButton.STATE_TOGGLED)

    def toggle_shutter_control(self, boolean):
        """
        :param boolean: True (on toggled) False (off toggled)
        """
        if boolean:
            self.shutter_control.button1.SetValue(LabeledDoubleToggleButton.STATE_TOGGLED)
            self.shutter_control.button2.SetValue(LabeledDoubleToggleButton.STATE_DEFAULT)
        else:
            self.shutter_control.button1.SetValue(LabeledDoubleToggleButton.STATE_DEFAULT)
            self.shutter_control.button2.SetValue(LabeledDoubleToggleButton.STATE_TOGGLED)

    @staticmethod
    def show_error(message):
        wx.MessageBox(message, 'Error', wx.OK | wx.ICON_ERROR)
