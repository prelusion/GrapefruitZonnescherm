from contextlib import contextmanager

import serial as pyserial
from serial.tools import list_ports


def get_com_ports():
    """ Get all serial ports in ((port, name), (port, name)) format. """
    ports = list(list_ports.comports())
    ports = [str(i) for i in ports]
    ports = [tuple(i.split(" - ")) for i in ports]
    return tuple(ports)


@contextmanager
def connect(port, baudrate=115200, timeout=0.5):
    connection = Connection(port, baudrate, timeout)
    connection.open()
    yield connection
    connection.close()


class Connection:
    def __init__(self, port, baudrate, timeout):
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._interface = None

    def open(self):
        self._interface = pyserial.Serial(
            port=self._port, baudrate=self._baudrate, bytesize=pyserial.EIGHTBITS,
            parity=pyserial.PARITY_NONE, stopbits=pyserial.STOPBITS_ONE, timeout=self._timeout)

    def close(self):
        self._interface.close()
        self._interface = None

    def write(self, data):
        if not self._interface:
            raise IOError("Connection must be opened before writing")

        if '\r' not in data:
            data += '\r'

        self._interface.write(data.encode())

    def readline(self):
        if not self._interface:
            raise IOError("Connection must be opened before reading")

        return self._interface.readline().decode()
