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
        apply_panel = wx.Panel(main_panel)

        # add panels to sizers
        main_sizer.Add(title_panel, 2, wx.EXPAND | wx.ALL)
        main_sizer.Add(settings_panel, 5, wx.EXPAND | wx.ALL)
        main_sizer.Add(apply_panel, 15, wx.EXPAND | wx.ALL)

        # Create content for title panel
        sizer = wx.GridSizer(2, 3, 0, 0)
        title_panel.SetSizer(sizer)
        sizer.Add(wx.StaticText(title_panel))

        settingText = wx.StaticText(title_panel, label="Settings:")
        settingText.SetFont(util.MainFont("title", fontsize=10))

        # add title to title panel
        sizer.Add(wx.StaticText())
        sizer.Add(settingText, flag=wx.ALIGN_CENTER)
        sizer.Add(wx.StaticText(title_panel))

        # Create settingspanel sizer
        settings_sizer = wx.GridSizer(7, 2, 0, 0)
        settings_panel.SetSizer(settings_sizer)

        # Create all settingslabels and inputs
        labels = [self.device_name_label, self.device_color_label, self.window_height_label, self.temp_treshold_label,
                  self.light_intens_label]
        self.inputs = {}
        self.input_names = {}

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
            self.input_names[k] = input_type
            settings_sizer.Add(input_type)

        # Create apply panel sizer
        # apply_sizer = wx.GridSizer(1, 2, 0, 0)
        # apply_panel.SetSizer(apply_sizer)
        # apply_panel.SetBackgroundColour(wx.BLUE)
        # Create apply button and add to sizer

        self.apply_button = wx.Button(settings_panel, label="Apply")
        # apply_sizer.Add(self.apply_button, flag=wx.ALIGN_CENTER)
        mocklabel2 = wx.StaticText(settings_panel, label="")
        settings_sizer.Add(mocklabel2)
        settings_sizer.Add(self.apply_button)

        self.delete_button = wx.Button(settings_panel, label="Delete unit")
        mocklabel = wx.StaticText(settings_panel, label="")
        settings_sizer.Add(mocklabel)
        settings_sizer.Add(self.delete_button)



        # apply_sizer.Add(self.delete_button, flag=wx.ALIGN_CENTER)

        settingsizer.Add(main_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_panel.Layout()

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
        for input in self.inputs.values():
            input.Disable()
        self.apply_button.Disable()

    def enable_inputs(self):
        for input in self.inputs.values():
            input.Enable()
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

    def show_success(self, message, title="Success"):
        wx.MessageBox(message, title, wx.OK | wx.ICON_INFORMATION)

    def show_error(self, message, title="Error"):
        wx.MessageBox(message, title, wx.OK | wx.ICON_ERROR)
