from src import mvc
import wx


class ControlUnitView(wx.Panel):
    def __init__(self):
        super().__init__(None, size=(450, 100))

        # Create main panel for control unit
        unit = wx.Panel(self, style=wx.BORDER_RAISED)
        unit.SetSize(500, 150)

        # Add gridsizer to main panel, 2 rows, 3 columns, 0 borders
        grid = wx.GridSizer(2, 3, 0, 0)
        unit.SetSizer(grid)

        # Create panel for device name
        name_panel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        name_panel.SetBackgroundColour((255, 255, 255))

        # Create namelabel
        self.name_label = wx.StaticText(name_panel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.name_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.name_label.SetFont(font)

        # align name label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.name_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        name_panel.SetSizer(main_sizer)

        # Panel for temperature readings
        temp_panel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        temp_panel.SetBackgroundColour((255, 255, 255))

        # initialize temperaturelabel
        self.temp_label = wx.StaticText(temp_panel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.temp_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.temp_label.SetFont(font)

        # align temperature label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.temp_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        temp_panel.SetSizer(main_sizer)

        # Create panel for device status
        status_panel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        status_panel.SetBackgroundColour((255, 255, 255))

        # Create statuslabel
        self.status_label = wx.StaticText(status_panel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.status_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.status_label.SetFont(font)


        # align  statuslabel to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.status_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        status_panel.SetSizer(main_sizer)

        # Create panel for device color (no label or positioning initializing needed)
        self.color_panel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        self.color_panel.SetBackgroundColour((1, 1, 1))

        # Create panel for connection status
        connection_panel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        connection_panel.SetBackgroundColour((255, 255, 255))

        # Initialize connection label
        self.connection_label = wx.StaticText(connection_panel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.connection_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.connection_label.SetFont(font)

        # Align connection label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.connection_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        connection_panel.SetSizer(main_sizer)

        # Create mode panel
        mode_panel = wx.Panel(unit, style=wx.SUNKEN_BORDER)
        mode_panel.SetBackgroundColour((255, 255, 255))

        # Create mode label
        self.mode_label = wx.StaticText(mode_panel, wx.ID_ANY, label="0", style=wx.ALIGN_CENTER)
        font = self.mode_label.GetFont()
        font.PointSize += 5
        font = font.Bold()
        self.mode_label.SetFont(font)

        # Align mode label to center
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer.Add(self.mode_label, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)
        mode_panel.SetSizer(main_sizer)

        # Add all panels to main device panel grid
        grid.Add(name_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(temp_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(status_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(self.color_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(connection_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)
        grid.Add(mode_panel, wx.ID_ANY, wx.EXPAND | wx.ALL)

    def setTemperature(self, temp):
        self.temp_label.SetLabelText(str(temp))

    def setName(self, name):
        self.name_label.SetLabelText(str(name))

    def setStatus(self, status):
        self.status_label.SetLabelText(str(status))

    def setDeviceCol(self, *color_tuple):
        self.color_panel.SetBackgroundColour(color_tuple)

    def setConnection(self, connection):
        self.connection_label.SetLabelText(str(connection))

    def setMode(self, mode):
        self.mode_label.SetLabelText(str(mode))
