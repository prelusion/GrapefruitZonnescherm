
import unittest

from src.controlunit import ControlUnitConnectionChecker


class TestSuite(unittest.TestCase):

    def test_control_unit_connection_checker(self):
        control_unit_connection_checker = ControlUnitConnectionChecker()



if __name__ == '__main__':
    unittest.main()
