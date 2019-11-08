import json
import os
import threading
import time
from decimal import Decimal
from random import randint
import wx

QUANTIZE_ONE_DIGIT = Decimal(10) ** -1  # e.g. Decimal(temp).quantize(util.QUANTIZE_ONE_DIGIT)


def deserialize_color(colorstring):
    colorstring = colorstring.split("(")[1].split(")")[0]
    r, g, b, a = colorstring.split(",")
    return int(r), int(g), int(b)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def timeout_exceeded(start, timeout):
    if not timeout or timeout == 0:
        return False

    return time.time() - start > timeout


def generate_16bit_int():
    return randint(1, 2 ** 16)


def encode_controlunit_id(app_id, controlunit_id):
    """
    :param app_id: int
    :param controlunit_id: int
    :return: 32-bit binary
    """
    return int(bin(app_id << 16 | controlunit_id), 2)


def decode_controlunit_id(id_):
    """
    :param id_: 32-bit binary
    :return: app_id: int, controlunit_id: int
    """
    return id_ >> 16, id_ & 0b1111111111111111


def load_json_from_file(filepath):
    if not os.path.exists(filepath):
        data = {}
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
            return data
    else:
        with open(filepath, "r") as f:
            return json.load(f)


def save_json_to_file(filepath, data):
    with threading.Lock():
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)


class MainFont(wx.Font):

    def __init__(self, texttype, fontsize=10, bold=False):
        super().__init__()
        self.SetFamily(wx.FONTFAMILY_SWISS)
        if texttype == "title":
            self.MakeBold()
            if fontsize is None:
                self.SetPointSize(12)
            else:
                self.SetPointSize(fontsize)
        elif texttype == "normal":
            if bold is True:
                self.MakeBold()
            self.SetPointSize(fontsize)
