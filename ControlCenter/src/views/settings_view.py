import wx

from src import mvc
from src import util


class SettingsView(mvc.View):

    def __init__(self, parent):
        super().__init__(parent)

        settingsizer = wx.GridSizer(1, 1, 0, 0)
        self.SetSizer(settingsizer)

        main_panel = wx.Panel(self)

        # Create label variables
        self.device_name_label = "Set device name: "
        self.device_color_label = "Set device color: "
        self.window_height_label = "Set window height: "
        self.temp_treshold_label = "Set temperature threshold: "
        self.light_intens_label = "Set light intensity threshold: "

        # Create main sizer and set to panel
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)

        # Create panels to fit in sizer
        title_panel = wx.Panel(main_panel)
        settings_panel = wx.Panel(main_panel)
        apply_outer_panel = wx.Panel(main_panel)
        apply_outer_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        apply_panel = wx.Panel(apply_outer_panel)
        apply_outer_panel_sizer.Add(apply_panel, wx.ID_ANY, wx.EXPAND | wx.ALL, 200)
        apply_outer_panel.SetSizer(apply_outer_panel_sizer)

        # add panels to sizers
        main_sizer.Add(title_panel, 2, wx.EXPAND | wx.ALL)
        main_sizer.Add(settings_panel, 5, wx.EXPAND | wx.ALL)
        main_sizer.Add(apply_outer_panel, 15, wx.EXPAND | wx.ALL)

        # Create content for title panel
        sizer = wx.GridSizer(2, 3, 0, 0)
        title_panel.SetSizer(sizer)
        sizer.Add(wx.StaticText(title_panel, label=""))
        setting_text = wx.StaticText(title_panel, label="Settings:       ")
        setting_text.SetFont(util.MainFont("title", fontsize=12))
        sizer.Add(setting_text, flag=wx.ALIGN_CENTER)
        sizer.Add(wx.StaticText(title_panel, label=""))

        # Create settingspanel sizer
        settings_sizer = wx.GridSizer(5, 2, 0, 0)
        settings_panel.SetSizer(settings_sizer)

        # Create all settingslabels and inputs
        labels = [self.device_name_label, self.device_color_label, self.window_height_label, self.temp_treshold_label,
                  self.light_intens_label]
        self.inputs = {}

        for k in labels:
            settings_label = wx.StaticText(settings_panel, label=k)
            settings_label.SetFont(util.MainFont("normal"))
            settings_sizer.Add(settings_label)
            if k == "Set device color: ":
                input_type = wx.ColourPickerCtrl(settings_panel)
                input_type.SetColour(wx.LIGHT_GREY)
            else:
                input_type = wx.TextCtrl(settings_panel)
            self.inputs[k] = input_type
            settings_sizer.Add(input_type)

        # Create apply panel sizer
        apply_sizer = wx.GridSizer(1, 2, 0, 0)
        apply_panel.SetSizer(apply_sizer)

        # Create apply button and add to sizer
        self.apply_button = wx.Button(apply_panel, label="Apply Settings")
        apply_sizer.Add(self.apply_button, flag=wx.ALIGN_CENTER)

        self.delete_button = wx.Button(apply_panel, label="Delete Unit")
        self.delete_button.Disable()
        apply_sizer.Add(self.delete_button, flag=wx.ALIGN_CENTER)

        settingsizer.Add(main_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_panel.Layout()

        self.disable_inputs()

    def get_settings(self):
        """
        :return: ['name', wx.Colour(0, 0, 0, 255), 'window', 'temp', 'intensity']
        """
        result = []
        for label in self.inputs:
            if type(self.inputs[label]) == wx.ColourPickerCtrl:
                result.append(self.inputs[label].GetColour())
            else:
                result.append(self.inputs[label].GetValue())
        return result

    def disable_inputs(self):
        for input_field in self.inputs.values():
            input_field.Disable()
        self.apply_button.Disable()

    def enable_inputs(self):
        for input_field in self.inputs.values():
            input_field.Enable()
        self.apply_button.Enable()

    def set_name(self, name):
        self.inputs[self.device_name_label].SetValue(str(name))

    def set_window_height(self, height):
        self.inputs[self.window_height_label].SetValue(str(height))

    def set_color(self, color):
        self.inputs[self.device_color_label].SetColour(color)

    def set_temperature_threshold(self, temp):
        self.inputs[self.temp_treshold_label].SetValue(str(temp))

    def set_light_intensity_threshold(self, light):
        self.inputs[self.light_intens_label].SetValue(str(light))

    @staticmethod
    def show_success(self, message, title="Success"):
        wx.MessageBox(message, title, wx.OK | wx.ICON_INFORMATION)

    @staticmethod
    def show_error(message, title="Error"):
        wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR)
