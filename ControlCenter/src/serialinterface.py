from contextlib import contextmanager
from logging import getLogger

import serial as pyserial
from serial.serialutil import SerialException
from serial.tools import list_ports

logger = getLogger(__name__)


def get_com_ports():
    """ Get all serial ports in ((port, name), (port, name)) format. """
    ports = list(list_ports.comports())
    ports = [str(i) for i in ports]
    ports = [tuple(i.split(" - "))[0] for i in ports]
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
        try:
            if self._interface:
                self._interface.close()
            self._interface = None
        except (OSError, SerialException):
            pass
        except Exception as e:
            logger.exception(e)

    def write(self, data):
        if not self._interface:
            raise IOError("Connection must be opened before writing")

        # logger.info(f"write serial data: {data}")

        if '\r' not in data:
            data += '\r'

        try:
            self._interface.write(data.encode())
        except (OSError, SerialException):
            pass
        except Exception as e:
            logger.exception(e)

    def readbuffer(self):
        if not self._interface:
            raise IOError("Connection must be opened before reading")

        try:
            data = self._interface.read(self._interface.inWaiting()).decode()
            # if data:
                # logger.info(f"read serial data: {data}")
            return data
        except (OSError, SerialException, UnicodeDecodeError):
            pass
        except Exception as e:
            logger.exception(e)

    def readline(self):
        if not self._interface:
            raise IOError("Connection must be opened before reading")

        try:
            return self._interface.readline().decode()
        except (OSError, SerialException, UnicodeDecodeError):
            pass
        except Exception as e:
            logger.exception(e)
