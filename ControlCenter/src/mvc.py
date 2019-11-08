import logging
import threading
from abc import ABC

logger = logging.getLogger(__name__)
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
        with threading.Lock():
            logger.info("[THREADING] enter lock")
            self.callbacks[func] = 1
        logger.info("[THREADING] exit lock")

    def del_callback(self, func):
        with threading.Lock():
            logger.info("[THREADING] enter lock")
            del self.callbacks[func]
        logger.info("[THREADING] exit lock")

    def _docallbacks(self, data):
        with threading.Lock():
            logger.info("[THREADING] enter lock")
            try:
                [func(self.model, data) for func in self.callbacks]
            except RuntimeError as e:
                logger.exception(e)
        logger.info("[THREADING] exit lock")

    def set(self, data):
        self.data = data
        self._docallbacks(self.data)

    def get(self):
        return self.data

    def unset(self):
        self.data = None
