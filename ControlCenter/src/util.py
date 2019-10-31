import json
import os
import threading
from decimal import Decimal
from random import randint
QUANTIZE_ONE_DIGIT = Decimal(10) ** -1  # e.g. Decimal(temp).quantize(util.QUANTIZE_ONE_DIGIT)


def generate_16bit_int():
    return randint(5, 99)


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
