import random

UNIT_COLORS = (
    (255, 0, 0),
    (255, 123, 0),
    (87, 6, 253),
    (1, 209, 126),
)


def randcolor():
    return random.choice(UNIT_COLORS)

print(randcolor())
