import wx

class test(wx.Frame):

    CHECKBOX_CONNECTED = "connected"
    CHECKBOX_STATUS_UP = "status up"
    CHECKBOX_STATUS_DOWN = "status down"
    CHECKBOX_SELECT_ALL = "select all"

    def __init__(self, parent):
        super().__init__(parent)
        self.SetTitle("test")

        checkbox_panel = wx.Panel(self)
        checkbox_panel.SetBackgroundColour((255, 255, 255))

        # Create vertical sizer and set sizer to checkboxpanel
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        checkbox_panel.SetSizer(vertical_sizer)

        # create an upper and lower panel and add horzontal sizers to it
        upperpanel = wx.Panel(checkbox_panel)
        lowerpanel = wx.Panel(checkbox_panel)

        # create sizers for upper and lower panel
        upper_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lower_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        upperpanel.SetSizer(upper_horizontal_sizer)
        lowerpanel.SetSizer(lower_horizontal_sizer)

        # add upper and lower panel to main sizer
        vertical_sizer.Add(upperpanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        vertical_sizer.Add(lowerpanel, wx.ID_ANY, wx.EXPAND | wx.ALL)


        checkboxes = [wx.CheckBox(upperpanel, label=self.CHECKBOX_CONNECTED), wx.CheckBox(upperpanel, label=self.CHECKBOX_STATUS_UP),
                       wx.CheckBox(lowerpanel, label=self.CHECKBOX_SELECT_ALL), wx.CheckBox(lowerpanel, label=self.CHECKBOX_STATUS_DOWN)]

        counter = 0
        for index in range(6):
            if index < 3:
                if index == 1:
                    upper_horizontal_sizer.AddSpacer(300)
                    print("spacing: ", index, "spacer object -upper")
                else:
                    upper_horizontal_sizer.Add(checkboxes[counter], wx.ID_ANY, wx.EXPAND | wx.ALL)
                    print("element: ", index, checkboxes[counter], " index in list: ", counter, " -upper")
                    counter += 1
            elif index >= 3:
                if index == 4:
                    lower_horizontal_sizer.AddSpacer(300)
                    print("spacing: ", index, "spacer object -lower")
                else:
                    lower_horizontal_sizer.Add(checkboxes[counter], wx.ID_ANY, wx.EXPAND | wx.ALL)
                    print("element: ", index, checkboxes[counter], " index in list: ", counter, " -lower")
                    counter += 1







app = wx.App(False)
window = test(None)
window.Show()
app.MainLoop()