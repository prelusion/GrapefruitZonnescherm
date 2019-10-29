
import unittest
import time
from src import controlunit
from src.models.controlunit import ControlUnitModel
from src import util


class TestSuite(unittest.TestCase):

    def test_control_unit_connection_checker(self):
        controlunit_manager = controlunit.ControlUnitManager()

        for i in range(15):
            print("TRY:", i)

            connected_ports = controlunit_manager.get_connected_ports()

            new_ports, down_ports = controlunit.get_online_control_units(skip=connected_ports)

            for port in down_ports:
                controlunit_manager.remove_unit(port)

            for port in new_ports:

                if controlunit_manager.is_port_connected(port):
                    continue

                comm = controlunit.ControlUnitCommunication(port)

                id_ = comm.get_id()
                if not id_:
                    comm.set_id(util.generate_id())

                model = ControlUnitModel(id_)

                controlunit_manager.add_unit(port, comm, model)

            print(controlunit_manager.get_units())
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
