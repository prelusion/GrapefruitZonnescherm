from abc import ABC
import wx
from copy import deepcopy


class Model(ABC):
    pass


class Controller(ABC):
    def __init__(self):
        self.view = None

    def set_view(self, view):
        self.view = view

    def get_view(self):
        return self.view


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

    def _docallbacks(self, prevstate, state):
        [func(prevstate, state) for func in self.callbacks]

    def set(self, data):
        prevstate = deepcopy(self.data)  # test this first without deepcopy, if weird bugs try deepcopy
        self.data = data
        self._docallbacks(prevstate, self.data)

    def get(self):
        return deepcopy(self.data)

    def unset(self):
        self.data = None
