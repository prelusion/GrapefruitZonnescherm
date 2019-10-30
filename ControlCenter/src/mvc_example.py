import wx
from src import mvc


class MoneyModel(mvc.Model):
    def __init__(self):
        self.money = mvc.Observable(0)

    def add_money(self, value):
        self.money.set(self.money.get() + value)

    def remove_money(self, value):
        self.money.set(self.money.get() - value)


class ShowMoneyView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent, title="Main View")

        sizer = wx.BoxSizer(wx.VERTICAL)

        text_label = wx.StaticText(self, label="My Money")
        self.money_label = wx.TextCtrl(self)
        self.money_label.SetEditable(False)

        sizer.Add(text_label, 0, wx.EXPAND | wx.ALL)
        sizer.Add(self.money_label, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)

    def set_money(self, money):
        self.money_label.SetValue(str(money))


class ChangeMoneyView(mvc.View):
    def __init__(self, parent):
        super().__init__(parent, title="Main View")
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.add_button = wx.Button(self, label="Add Money")
        self.remove_button = wx.Button(self, label="Remove Money")

        sizer.Add(self.add_button, 0, wx.EXPAND | wx.ALL)
        sizer.Add(self.remove_button, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)


class Controller(mvc.Controller):
    def __init__(self, app):
        super().__init__(app)

        self.model = MoneyModel()

        self.show_money_view = ShowMoneyView(None)
        self.change_money_view = ChangeMoneyView(self.show_money_view)

        self.on_money_changed(self.model.money.get())

        self.change_money_view.add_button.Bind(wx.EVT_BUTTON, self.add_money)
        self.change_money_view.remove_button.Bind(wx.EVT_BUTTON, self.remove_money)

        self.model.money.add_callback(self.on_money_changed)

        self.show_money_view.Show()
        self.change_money_view.Show()

    def add_money(self, e):
        self.model.add_money(10)

    def remove_money(self, e):
        self.model.remove_money(10)

    def on_money_changed(self, money):
        self.show_money_view.set_money(money)


app = wx.App(False)
controller = Controller(app)
app.MainLoop()
