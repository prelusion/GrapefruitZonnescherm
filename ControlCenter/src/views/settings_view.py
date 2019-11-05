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

        self.deviceName = Setting(self,"Set device name:")
        sizer.Add(self.deviceName, flag=wx.ALIGN_CENTER | wx.ALL)

        self.windowHeight = Setting(self,"Set window height:")
        sizer.Add(self.windowHeight, flag=wx.ALIGN_CENTER | wx.ALL)

        self.deviceColor = Setting(self,"Set device color:")
        sizer.Add(self.deviceColor, flag=wx.ALIGN_CENTER | wx.ALL)

    def SetName(self, name):
        self.deviceName.SetValue(name)

    def SetHeight(self, height):
        self.windowHeight.SetValue(height)

    def SetColor(self, color):
        self.deviceColor.SetValue(color)



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
        sizer.Add(input, flag=wx.ALIGN_LEFT)

    def SetValue(self, value):
        self.input.SetValue(value)