from abc import ABC
from copy import deepcopy

import wx


class Model(ABC):
    pass


class Controller(ABC):
    pass


class View(wx.Panel):
    pass


class Observable:
    def __init__(self, model, value=None):
        self.model = model
        self.data = value
        self.callbacks = {}

    def add_callback(self, func):
        self.callbacks[func] = 1

    def del_callback(self, func):
        del self.callbacks[func]

    def _docallbacks(self, data):
        [func(self.model, data) for func in self.callbacks]

    def set(self, data):
        self.data = data
        self._docallbacks(self.data)

    def get(self):
        return self.data

    def unset(self):
        self.data = None
