from contextlib import contextmanager
from logging import getLogger

import serial as pyserial
from serial.serialutil import SerialException
from serial.tools import list_ports
from src.decorators import retry_on_any_exception

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


RETRIES = 10


class Connection:
    def __init__(self, port, baudrate, timeout):
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._interface = None

    @retry_on_any_exception(RETRIES)
    def open(self):
        self._interface = pyserial.Serial(
            port=self._port, baudrate=self._baudrate, bytesize=pyserial.EIGHTBITS,
            parity=pyserial.PARITY_NONE, stopbits=pyserial.STOPBITS_ONE, timeout=self._timeout)

    @retry_on_any_exception(RETRIES)
    def close(self):

        if self._interface:
            self._interface.close()
        self._interface = None

    @retry_on_any_exception(RETRIES)
    def write(self, data):
        if not self._interface:
            raise IOError("Connection must be opened before writing")

        # logger.info(f"write serial data: {data}")

        if '\r' not in data:
            data += '\r'

        self._interface.write(data.encode())

    @retry_on_any_exception(RETRIES)
    def readbuffer(self):
        if not self._interface:
            raise IOError("Connection must be opened before reading")

        data = self._interface.read(self._interface.inWaiting()).decode()
        # if data:
            # logger.info(f"read serial data: {data}")
        return data

    @retry_on_any_exception(RETRIES)
    def readline(self):
        if not self._interface:
            raise IOError("Connection must be opened before reading")

        return self._interface.readline().decode()


"""
except (Exception, OSError, SerialException) as e:
            logger.exception(e)
            
            """