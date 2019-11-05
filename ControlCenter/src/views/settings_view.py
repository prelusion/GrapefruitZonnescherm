import wx

from src import mvc


class SettingsView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((100, 255, 100))

        sizer = wx.GridSizer(14,1,0,0)

        sizer.Add(wx.StaticText(self))
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        settingText = wx.StaticText(self, label="Settings:")
        settingText.SetFont(font)
        sizer.Add(settingText, flag=wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(wx.StaticLine(self, pos=(25, 50), size=(600, 1)), flag= wx.ALL | wx.ALIGN_CENTER)

        self.SetSizer(sizer)

        self.device_name = Setting(self,"Set device name:")
        sizer.Add(self.device_name, flag=wx.ALIGN_CENTER | wx.ALL)

        self.window_height = Setting(self,"Set window height:")
        sizer.Add(self.window_height, flag=wx.ALIGN_CENTER | wx.ALL)

        self.device_color = Setting(self,"Set device color:")
        sizer.Add(self.device_color, flag=wx.ALIGN_CENTER | wx.ALL)

        self.max_temp = Setting(self,"Set temperature threshold:")
        sizer.Add(self.max_temp, flag=wx.ALIGN_CENTER | wx.ALL)

        self.max_light = Setting(self,"Set light sensitivity threshold:")
        sizer.Add(self.max_light, flag=wx.ALIGN_CENTER | wx.ALL)

        self.apply_button = wx.Button(self, label="apply")
        sizer.Add(self.apply_button)

    def set_name(self, name):
        self.device_name.set_value(name)

    def set_height(self, height):
        self.window_height.set_value(height)

    def set_color(self, color):
        self.device_name.set_value(color)

    def set_max_temp(self, color):
        self.max_temp.set_value(color)

    def set_max_light(self, color):
        self.max_light.SetValue(color)


    def get_name(self):
        return self.device_name.get_value()

    def get_height(self):
        return self.window_height.get_value()

    def get_color(self):
        return self.device_name.get_value()

    def get_max_temp(self):
        return self.max_temp.get_value()

    def get_max_light(self):
        return self.max_light.get_value()

class Setting(mvc.View):
    def __init__(self, parent, text):
        super().__init__(parent)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        sizer = wx.GridSizer(1,5,0,0)
        self.SetSizer(sizer)
        textField = wx.StaticText(self, label=text)
        textField.SetFont(font)
        sizer.Add(wx.StaticText(self), flag=wx.ALIGN_LEFT)
        sizer.Add(textField, flag=wx.ALIGN_LEFT)
        sizer.Add(wx.StaticText(self), flag=wx.ALIGN_LEFT)

        self.input = wx.TextCtrl(self, size=(80,20),value="test")
        sizer.Add(self.input, flag=wx.ALIGN_LEFT)

    def set_value(self, value):
        self.input.SetValue(value)

    def get_value(self):
        return self.input.GetValue()