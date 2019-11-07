from collections import namedtuple

Measurement = namedtuple("Measurement", ["timestamp",
                                         "temperature",
                                         "shutter_status",
                                         "light_intensity"])
