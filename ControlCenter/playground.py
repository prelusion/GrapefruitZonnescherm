import wx


class test(wx.Frame):

    def __init__(self, title):
        super().__init__(None, title=title, size=(550, 150))
        # Create main panel for control unit
        unit = wx.Panel(self, style=wx.BORDER_RAISED)
        unit.SetSize(500, 150)

        # Add gridsizer to main panel, 2 rows, 3 columns, 0 borders
        grid = wx.GridSizer(2, 3, 0, 0)
        unit.SetSizer(grid)

        # Create panel for device name
        namepanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        namepanel.SetBackgroundColour((255, 255, 255))

        # Create namelabel
        self.namelabel = wx.StaticText(namepanel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.namelabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.namelabel.SetFont(font)

        # align name label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.namelabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        namepanel.SetSizer(main_sizer)

        # Panel for temperature readings
        temppanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        temppanel.SetBackgroundColour((255, 255, 255))

        # initialize temperaturelabel
        self.templabel = wx.StaticText(temppanel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.templabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.templabel.SetFont(font)

        # align temperature label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.templabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        temppanel.SetSizer(main_sizer)

        # Create panel for device status
        statuspanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        statuspanel.SetBackgroundColour((255, 255, 255))

        # Create statuslabel
        self.statuslabel = wx.StaticText(statuspanel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.statuslabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.statuslabel.SetFont(font)

        # align  statuslabel to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.statuslabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        statuspanel.SetSizer(main_sizer)

        # Create panel for device color (no label or positioning initializing needed)
        self.colorpanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        self.colorpanel.SetBackgroundColour((1,1,1))

        # Create panel for connection status
        connectionpanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        connectionpanel.SetBackgroundColour((255, 255, 255))

        # Initialize connection label
        self.connectionlabel = wx.StaticText(connectionpanel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.connectionlabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.connectionlabel.SetFont(font)

        # Align connection label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.connectionlabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        connectionpanel.SetSizer(main_sizer)

        # Create mode panel
        modepanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        modepanel.SetBackgroundColour((255, 255, 255))

        # Create mode label
        self.modelabel = wx.StaticText(modepanel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.modelabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.modelabel.SetFont(font)

        # Align mode label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.modelabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        modepanel.SetSizer(main_sizer)

        # Add all panels to main device panel grid
        grid.Add(namepanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(temppanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(statuspanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(self.colorpanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(connectionpanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(modepanel, wx.ID_ANY, wx.EXPAND | wx.ALL)


    def setTemperature(self, temp):
        self.templabel.SetLabelText(str(temp) + "°C")

    def setName(self, name):
        self.namelabel.SetLabelText(str(name))

    def setStatus(self, status):
        self.statuslabel.SetLabelText(str(status))

    def setDeviceCol(self, *colorTuple):
        self.colorpanel.SetBackgroundColour(colorTuple)

    def setConnection(self, connection):
        self.connectionlabel.SetLabelText(str(connection))

    def setMode(self, mode):
        self.modelabel.SetLabelText(str(mode))

app = wx.App(False)
mainview = test("Grapefruit controlpanel")
mainview.SetBackgroundColour((23,55,76))
mainview.setConnection("connected")
mainview.setMode("automatic")
mainview.setStatus("shutter up")
mainview.setName("arduino 1")
mainview.setTemperature(12)
mainview.Show()
app.MainLoop()


