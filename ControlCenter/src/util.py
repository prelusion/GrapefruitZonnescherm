from random import randint
from decimal import Decimal


QUANTIZE_ONE_DIGIT = Decimal(10) ** -1  # e.g. Decimal(temp).quantize(util.QUANTIZE_ONE_DIGIT)


def generate_id():

    return randint(1, 2**16)
