import json
import os
import threading
from decimal import Decimal
from random import randint
QUANTIZE_ONE_DIGIT = Decimal(10) ** -1  # e.g. Decimal(temp).quantize(util.QUANTIZE_ONE_DIGIT)


def generate_16bit_int():
    return randint(1, 2 ** 16)


def encode_controlunit_id(app_id, controlunit_id):
    return bin(app_id << 16 | controlunit_id)


def decode_controlunit_id(id_):
    """
    :param binary_id: 32-bit int
    :return: app_id, controlunit_id
    """
    return int(bin(int(id_, 2) >> 16), 2), int(bin(int(id_, 2) & 0b1111111111111111), 2)


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
