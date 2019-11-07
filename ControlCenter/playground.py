import wx
from src import mvc
import pprint

class test(wx.Frame):


    def __init__(self, parent):
        super().__init__(parent)
        self.SetTitle("test")

        main_panel = wx.Panel(self)

        # Create label variables
        self.device_name_label = "Set device name: "
        self.device_color_label = "Set device color: "
        self.window_height_label = "Set window height: "
        self.temp_treshold_label = "Set temperature treshold: "
        self.light_intens_label = "Set light intensety treshold: "

        # Create main sizer and set to panel
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)

        # Create panels to fit in sizer
        title_panel = wx.Panel(main_panel)
        settings_panel = wx.Panel(main_panel)
        settings_panel.SetBackgroundColour((255, 255, 255))
        settings_panel.SetWindowStyle(wx.BORDER_SIMPLE)
        apply_panel = wx.Panel(main_panel)
        apply_panel.SetBackgroundColour((200,1,111))

        # add panels to sizers
        main_sizer.Add(title_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(settings_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(apply_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

        # Create content for title panel
        sizer = wx.GridSizer(2,3,0,0)
        title_panel.SetSizer(sizer)
        sizer.Add(wx.StaticText(title_panel))

        settingText = wx.StaticText(title_panel, label="Settings:")
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        settingText.SetFont(font)

        # add title to title panel
        sizer.Add(wx.StaticText())
        sizer.Add(settingText, flag=wx.ALIGN_CENTER)
        sizer.Add(wx.StaticText(title_panel))

        # add line to title panel
        sizer.Add(wx.StaticText(title_panel))
        sizer.Add(wx.StaticLine(title_panel, pos=(25, 50), size=(600, 1)), flag= wx.ALL | wx.ALIGN_CENTER)
        sizer.Add(wx.StaticText(title_panel))

        # Create settingspanel sizer
        settings_sizer = wx.GridSizer(5, 2,0,0)
        settings_panel.SetSizer(settings_sizer)

        # Create all settingslabels and inputs
        labels = [self.device_name_label, self.device_color_label, self.window_height_label, self.temp_treshold_label, self.light_intens_label]
        self.inputs = {}

        for k in labels:
            settings_sizer.Add(wx.StaticText(settings_panel, label=k))
            if k == "Set device color: ":
                input_type = wx.ColourPickerCtrl(settings_panel)
            else:
                input_type = wx.TextCtrl(settings_panel)
            self.inputs[k] = input_type
            settings_sizer.Add(input_type)
        pprint.pprint(self.inputs)

        # Create apply panel sizer
        apply_sizer = wx.GridSizer(1,1,0,0)
        apply_panel.SetSizer(apply_sizer)

        # Create apply button and add to sizer
        self.apply_button = wx.Button(apply_panel, label="apply")
        apply_sizer.Add(self.apply_button, flag=wx.ALIGN_CENTER)


    def onclick(self, e):
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

app = wx.App(False)
window = test(None)
window.Show()
app.MainLoop()