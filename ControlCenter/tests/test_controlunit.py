
import unittest

from src import controlunit


class TestSuite(unittest.TestCase):

    def test_control_unit_connection_checker(self):
        ports = controlunit.get_online_control_units()
        print("PORTS:", ports)


if __name__ == '__main__':
    unittest.main()
