import wx

from src import mvc


class SettingsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.GridSizer(16,3,0,0)
        self.SetSizer(sizer)
        sizer.Add(wx.StaticText(self))
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        settingText = wx.StaticText(self, label="Settings:")
        settingText.SetFont(font)

        sizer.Add(wx.StaticText())
        sizer.Add(settingText, flag=wx.ALIGN_CENTER)
        sizer.Add(wx.StaticText(self))

        sizer.Add(wx.StaticText(self))
        sizer.Add(wx.StaticLine(self, pos=(25, 50), size=(600, 1)), flag= wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(wx.StaticText(self))

        self.device_name = Setting(self,"Set device name: ", "", sizer)
        #sizer.Add(self.device_name, flag=wx.ALIGN_LEFT | wx.ALL)

        self.window_height = Setting(self,"Set window height:", " cm", sizer)
        #sizer.Add(self.window_height, flag=wx.ALIGN_LEFT | wx.ALL)

        self.device_color = Setting(self,"Set device color:", "", sizer)
        #sizer.Add(self.device_color, flag=wx.ALIGN_LEFT | wx.ALL)

        self.max_temp = Setting(self,"Set temperature threshold:", " ℃", sizer)
        #sizer.Add(self.max_temp, flag=wx.ALIGN_LEFT | wx.ALL)

        self.max_light = Setting(self,"Set light sensitivity threshold:", " cd", sizer)
        sizer.Add(self.max_light, flag=wx.ALIGN_LEFT | wx.ALL)

        self.apply_button = wx.Button(self, label="apply")
        sizer.Add(self.apply_button, flag=wx.ALIGN_CENTER)

    def disable_inputs(self):
        self.device_name.Disable()
        self.window_height.Disable()
        self.device_name.Disable()
        self.window_height.Disable()
        self.device_color.Disable()
        self.max_temp.Disable()
        self.max_light.Disable()
        self.apply_button.Disable()

    def enable_inputs(self):
        self.device_name.Enable()
        self.window_height.Enable()
        self.device_name.Enable()
        self.window_height.Enable()
        self.device_color.Enable()
        self.max_temp.Enable()
        self.max_light.Enable()
        self.apply_button.Enable()

    def set_name(self, name):
        self.device_name.set_value(name)

    def set_window_height(self, height):
        self.window_height.set_value(height)

    def set_color(self, color):
        self.device_name.set_value(color)

    def set_temperature_threshold(self, color):
        self.max_temp.set_value(color)

    def set_light_intensity_threshold(self, light):
        self.max_light.set_value(light)


    def get_name(self):
        return self.device_name.get_value()

    def get_window_height(self):
        return self.window_height.get_value()

    def get_color(self):
        return self.device_name.get_value()

    def get_temperature_threshold(self):
        return self.max_temp.get_value()

    def get_light_intensity_threshold(self):
        return self.max_light.get_value()

class Setting(mvc.View):
    def __init__(self, parent, prefix, subfix, sizer):
        super().__init__(parent)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.pre_fix = wx.StaticText(parent, label=prefix)
        self.pre_fix.SetFont(font)
        self.sub_fix = wx.StaticText(parent, label=subfix)
        self.sub_fix.SetFont(font)
        self.input = wx.TextCtrl(parent, size=(80, 20), value="")
        sizer.Add(self.pre_fix, flag=wx.ALIGN_LEFT | wx.ALL)
        sizer.Add(self.input, flag=wx.ALIGN_RIGHT | wx.ALL)
        sizer.Add(self.sub_fix, flag= wx.ALIGN_LEFT | wx.ALL)

    def set_value(self, value):
        self.input.SetValue(str(value))

    def get_value(self):
        return self.input.GetValue()

    def Disable(self):
        self.input.Disable()

    def Enable(self, **kwargs):
        self.input.Enable()
