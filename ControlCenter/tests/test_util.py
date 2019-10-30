import unittest
from src import util
import re

class TestSuite(unittest.TestCase):

    def test_list_difference_1(self):
        prev = [2, 4, 8]
        now = [2, 4, 8, 9]
        new = set(now) - set(prev)
        self.assertEqual(list(new), [9])

    def test_list_difference_2(self):
        prev = [2, 4, 8]
        now = [2, 8, 9]
        new = set(now) - set(prev)
        self.assertEqual(list(new), [9])

    def test_generate_id(self):
        app_id = util.generate_id()
        cu_id_1 = util.generate_id()
        cu_id_2 = util.generate_id()
        cu_id_3 = util.generate_id()

        print(app_id, cu_id_1, cu_id_2, cu_id_3, sep=", ")

        app_cu_id_1 = bin(app_id) + bin(cu_id_1)
        app_cu_id_2 = bin(app_id) + bin(cu_id_2)
        app_cu_id_3 = bin(app_id) + bin(cu_id_3)
        print(app_cu_id_1, app_cu_id_2, app_cu_id_3, sep=", ")


if __name__ == '__main__':
    unittest.main()
