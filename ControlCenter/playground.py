import wx
from src import mvc

class test(wx.Frame):

    settings = {}

    def __init__(self, parent):
        super().__init__(parent)
        self.SetTitle("test")

        # Create main sizer and set to panel
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(main_sizer)


        # Create panels to fit in sizer
        title_panel = wx.Panel(self)
        settings_panel = wx.Panel(self)
        settings_panel.SetBackgroundColour((255, 255, 255))
        settings_panel.SetWindowStyle(wx.BORDER_SIMPLE)
        apply_panel = wx.Panel(self)
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



        settings_sizer = wx.GridSizer(5, 2,0,0)
        settings_panel.SetSizer(settings_sizer)

        self.device_name_label = wx.StaticText(settings_panel)
        self.device_name_label.SetLabelText("Set device name: ")
        settings_sizer.Add(self.device_name_label)

        self.device_name_input = wx.TextCtrl(settings_panel)
        settings_sizer.Add(self.device_name_input)


        self.window_height_label = wx.StaticText(settings_panel)
        self.window_height_label.SetLabelText("Set window height: ")
        settings_sizer.Add(self.window_height_label)

        self.window_height_input = wx.TextCtrl(settings_panel)
        settings_sizer.Add(self.window_height_input)

        self.device_color_label = wx.StaticText(settings_panel)
        self.device_color_label.SetLabelText("Set device color: ")
        settings_sizer.Add(self.device_color_label)

        self.device_color_input = wx.ColourPickerCtrl(settings_panel)
        settings_sizer.Add(self.device_color_input)

        self.max_temp_label = wx.StaticText(settings_panel)
        self.max_temp_label.SetLabelText("Set temperature treshold: ")
        settings_sizer.Add(self.max_temp_label)

        self.max_temp_input = wx.TextCtrl(settings_panel)
        settings_sizer.Add(self.max_temp_input)

        self.light_intensity_label = wx.StaticText(settings_panel)
        self.light_intensity_label.SetLabelText("Set light intensety treshold: ")
        settings_sizer.Add(self.light_intensity_label)

        self.light_intensity_input = wx.TextCtrl(settings_panel)
        settings_sizer.Add(self.light_intensity_input)










        # panel1 = wx.Panel(settings_panel)
        # panel2 = wx.Panel(settings_panel)
        # panel3 = wx.Panel(settings_panel)
        # panel4 = wx.Panel(settings_panel)
        # panel5 = wx.Panel(settings_panel)
        # panel6 = wx.Panel(settings_panel)
        # panel7 = wx.Panel(settings_panel)
        # panel8 = wx.Panel(settings_panel)
        # panel9 = wx.Panel(settings_panel)
        # panel10 = wx.Panel(settings_panel)
        #
        # panel1.SetBackgroundColour((252, 186, 3))
        # panel2.SetBackgroundColour((0, 0, 0))
        # panel3.SetBackgroundColour((51, 255, 0))
        # panel4.SetBackgroundColour((0, 247, 255))
        # panel5.SetBackgroundColour((81, 0, 255))
        # panel6.SetBackgroundColour((153, 0, 25))
        # panel7.SetBackgroundColour((255, 0, 208))
        # panel8.SetBackgroundColour((255, 0, 106))
        # panel9.SetBackgroundColour((255, 0, 0))
        # panel10.SetBackgroundColour((255,255,255))
        #
        #
        # settings_sizer.Add(panel1, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel2, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel3, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel4, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel5, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel6, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel7, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel8, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel9, wx.ID_ANY, wx.EXPAND | wx.ALL)
        # settings_sizer.Add(panel10, wx.ID_ANY, wx.EXPAND | wx.ALL)






























        # Create apply panel sizer
        apply_sizer = wx.GridSizer(1,1,0,0)
        apply_panel.SetSizer(apply_sizer)

        # Create apply button and add to sizer
        self.apply_button = wx.Button(apply_panel, label="apply")
        apply_sizer.Add(self.apply_button, flag=wx.ALIGN_CENTER)



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
        self.input.SetValue(value)

    def get_value(self):
        return self.input.GetValue()

    def Disable(self):
        self.input.Disable()

    def Enable(self, **kwargs):
        self.input.Enable()



app = wx.App(False)
window = test(None)
window.Show()
app.MainLoop()