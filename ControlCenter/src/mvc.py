from abc import ABC
import wx


class Model(ABC):
    pass


class Controller(ABC):
    def __init__(self, app):
        self.app = app


class View(wx.Panel):
    pass


class Observable:
    def __init__(self, value=None):
        self.data = value
        self.callbacks = {}

    def add_callback(self, func):
        self.callbacks[func] = 1

    def del_callback(self, func):
        del self.callbacks[func]

    def _docallbacks(self):
        [func(self.data) for func in self.callbacks]

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None
