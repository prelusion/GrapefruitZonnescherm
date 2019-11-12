import logging
import threading
from abc import ABC

import wx

logger = logging.getLogger(__name__)


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
        with threading.Lock():
            self.callbacks[func] = 1

    def del_callback(self, func):
        with threading.Lock():
            del self.callbacks[func]

    def _docallbacks(self, data):
        with threading.Lock():
            try:
                [func(self.model, data) for func in self.callbacks]
            except RuntimeError as e:
                logger.exception(e)

    def set(self, data):
        self.data = data
        self._docallbacks(self.data)

    def get(self):
        return self.data

    def unset(self):
        self.data = None
