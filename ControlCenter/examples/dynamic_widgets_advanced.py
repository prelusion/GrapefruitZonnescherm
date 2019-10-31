import wx


class Panel(wx.Panel):
    def __init__(self, app, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.parent = parent
        self.main_sizer = None

    def set_sizer(self, sizer):
        self.SetSizer(sizer)
        self.main_sizer = sizer

    def refresh(self):
        print("refresh panel")
        if self.main_sizer:
            self.main_sizer.Layout()


class TopFrame(wx.Frame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.app = app
        self.main_sizer = None

    def set_sizer(self, sizer):
        self.SetSizer(sizer)
        self.main_sizer = sizer

    def refresh(self):
        print("refresh top frame")
        if self.main_sizer:
            self.main_sizer.Layout()


class ConcretePanelA(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn = wx.Button(self, label="Add")
        self.btn.Bind(wx.EVT_BUTTON, self.on_add_widget)
        main_sizer.Add(self.btn, 0, wx.CENTER|wx.ALL, 5)

        self.SetBackgroundColour((255, 0, 0))
        self.set_sizer(main_sizer)

    def on_add_widget(self, event):
        new_button = wx.Button(self, label="Hi")
        self.main_sizer.Add(new_button, 0, wx.ALL, 5)
        self.main_sizer.Layout()


class ConcretePanelB(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetBackgroundColour((0, 255, 0))


class ConcreteTopFrame(TopFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        concrete_panel_a = ConcretePanelA(self.app, self)
        concrete_panel_b = ConcretePanelB(self.app, self)

        main_sizer.Add(concrete_panel_a, wx.ID_ANY, wx.EXPAND | wx.ALL)
        main_sizer.Add(concrete_panel_b, wx.ID_ANY, wx.EXPAND | wx.ALL)

        self.set_sizer(main_sizer)
        print("done")


if __name__ == "__main__":
    app = wx.App(False)
    frame = ConcreteTopFrame(app, size=(1200, 700))
    frame.Show()
    app.MainLoop()
