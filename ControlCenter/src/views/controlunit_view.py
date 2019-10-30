from src import mvc
import wx


class ControlUnitView(wx.Panel):
    def __init__(self):
        super().__init__(None, size=(550, 150))

        # Initialize readings
        self.temperature = "0°C"
        self.name = "device1"
        self.status = "disconnected"
        self.devicecol = (255, 50, 1)
        self.connection = "disonnected"
        self.mode = "disconnected"

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
        namelabel = wx.StaticText(namepanel, wx.ID_ANY, label=str(self.name), style=wx.ALIGN_CENTER)
        font = namelabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        namelabel.SetFont(font)

        # align name label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(namelabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        namepanel.SetSizer(main_sizer)

        # Panel for temperature readings
        temppanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        temppanel.SetBackgroundColour((255, 255, 255))

        # initialize temperaturelabel
        templabel = wx.StaticText(temppanel, wx.ID_ANY, label=str(self.temperature), style=wx.ALIGN_CENTER)
        font = templabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        templabel.SetFont(font)

        # align temperature label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(templabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        temppanel.SetSizer(main_sizer)

        # Create panel for device status
        statuspanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        statuspanel.SetBackgroundColour((255, 255, 255))

        # Create statuslabel
        statuslabel = wx.StaticText(statuspanel, wx.ID_ANY, label=str(self.status), style=wx.ALIGN_CENTER)
        font = statuslabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        statuslabel.SetFont(font)

        # align  statuslabel to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(statuslabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        statuspanel.SetSizer(main_sizer)

        # Create panel for device color (no label or positioning initializing needed)
        colorpanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        colorpanel.SetBackgroundColour(self.devicecol)

        # Create panel for connection status
        connectionpanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        connectionpanel.SetBackgroundColour((255, 255, 255))

        # Initialize connection label
        connectionlabel = wx.StaticText(connectionpanel, wx.ID_ANY, label=str(self.connection), style=wx.ALIGN_CENTER)
        font = connectionlabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        connectionlabel.SetFont(font)

        # Align connection label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(connectionlabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        connectionpanel.SetSizer(main_sizer)

        # Create mode panel
        modepanel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        modepanel.SetBackgroundColour((255, 255, 255))

        # Create mode label
        modelabel = wx.StaticText(modepanel, wx.ID_ANY, label=str(self.mode), style=wx.ALIGN_CENTER)
        font = modelabel.GetFont()
        font.PointSize += 10
        font = font.Bold()
        modelabel.SetFont(font)

        # Align mode label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(modelabel, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        modepanel.SetSizer(main_sizer)

        # Add all panels to main device panel grid
        grid.Add(namepanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(temppanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(statuspanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(colorpanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(connectionpanel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(modepanel, wx.ID_ANY, wx.EXPAND | wx.ALL)

    def setTemperature(self, temp):
        self.temperature = str(temp) + "°C"

    def setName(self, name):
        self.name = str(name)

    def setStatus(self, status):
        self.status = str(status)

    def setDeviceCol(self, *colorTuple):
        self.devicecol = colorTuple

    def setConnection(self, connection):
        self.connection = str(connection)

    def setMode(self, mode):
        self.mode = str(mode)