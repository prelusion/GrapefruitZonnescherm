import time
from collections import namedtuple
import threading
from src import serialinterface as ser

BAUDRATE = 38400

SensorData = namedtuple("SensorData", ["timestamp",
                                       "temperature",
                                       "shutter_status",
                                       "light_sensitivity"])

Measurement = namedtuple("Measurement", ["timestamp", "value"])


def get_online_control_units():
    """
    Example:

        cu_manager = ControlUnitManager()

        ports = get_online_control_units()

        for port in ports:
            cu_comm = ControlUnitCommunication(port)

            id = cu_comm.get_id()
            if not id:
                cu_comm.set_id(generate_id())

            cu_model = ControlUnitModel(id)

            cu_manager.add_unit(cu_comm, cu_model)

        while True:
            cu_manager.update_models()
            time.sleep(60)




    Example with dynamic control unit connection:

        cu_manager = ControlUnitManager()


        def port_check_service:
            previous_ports = []

            while True:
                ports = get_online_control_units()

                new_ports = set(ports) - set(previous_ports)

                for port in new_ports:
                    cu_comm = ControlUnitCommunication(port)

                    id = cu_comm.get_id()
                    if not id:
                        cu_comm.set_id(generate_id())

                    cu_model = ControlUnitModel(id)

                    cu_manager.add_unit(cu_comm, cu_model)

                time.sleep(5)


        def sensor_data_service:
            while True:
                cu_manager.update_models()
                time.sleep(60)
    """

    online_ports = []

    def test_port(port, name):
        nonlocal online_ports

        with ser.connect(port, baudrate=BAUDRATE, timeout=1) as conn:
            for i in range(15):
                conn.write("PING")
                data = conn.readbuffer()
                if "PONG" in data:
                    online_ports.append((port, name))
                    return
                time.sleep(0.1)

    threads = []
    for port, name in ser.get_com_ports():
        t = threading.Thread(target=test_port, args=(port, name))
        threads.append(t)
        t.start()

    [t.join() for t in threads]

    return online_ports


class ControlUnitCommunication:
    def __init__(self, port):
        self.id = None
        self._com_port = port
        self._serial_connection = None

    def get_id(self):
        pass

    def is_online(self):
        pass

    def get_shutter_status(self):
        pass

    def get_sensor_data(self):
        return SensorData(time.time(), 5, 5, 5)

    def get_sensor_history(self):
        pass

    def _get_connection(self):
        if not self._serial_connection:
            self._serial_connection = ser.Connection(self._com_port, BAUDRATE, timeout=0.1)
        return self._serial_connection


class ControlUnitManager:
    def __init__(self):
        self._units = []

    def add_unit(self, communication, model):
        self._units.append((communication, model))

    def get_units(self):
        return self._units

    def update_models(self):
        for i, unit in enumerate(self._units.copy()):
            comm, model = unit

            data = comm.get_sensor_data()

            if not data:
                del self._units[i]

            model.add_temperature(Measurement(data.timestamp, data.temperature))
            model.add_shutter_status(Measurement(data.timestamp, data.shutter_status))
            model.add_light_sensitivity(Measurement(data.timestamp, data.light_sensitivity))


if __name__ == "__main__":
    get_online_control_units()
