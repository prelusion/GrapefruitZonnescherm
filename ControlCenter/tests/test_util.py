import unittest

from src import util
from math import sqrt


class TestSuite(unittest.TestCase):

    def test_generate_id_2(self):
        app_id = util.generate_16bit_int()
        cu_id_1 = util.generate_16bit_int()
        cu_id_2 = util.generate_16bit_int()
        print("app_id", app_id)
        print("cu_id_1", cu_id_1)
        print("cu_id_2", cu_id_2)
        id1 = util.encode_controlunit_id(app_id, cu_id_1)
        id2 = util.encode_controlunit_id(app_id, cu_id_2)
        print("id1", id1)
        print("id2", id2)
        app_id_back, cu_id_1_back = util.decode_controlunit_id(id1)
        app_id_back2, cu_id_2_back = util.decode_controlunit_id(id2)
        print("app_id_back_1", app_id_back)
        print("cu_id_1_back", cu_id_1_back)
        print("app_id_back_2", app_id_back2)
        print("cu_id_2_back", cu_id_2_back)


    @unittest.skip
    def test_generate_id(self):
        app_id = util.generate_16bit_int()
        cu_id_1 = util.generate_16bit_int()
        cu_id_2 = util.generate_16bit_int()
        print("app_id", app_id)
        print("cu_id_1", cu_id_1)
        print("cu_id_2", cu_id_2)

        # id_1 = (int(bin(app_id).split("0b")[1]) << 16) + int(bin(cu_id_1).split("0b")[1])
        id_1 = bin(app_id << 16 | cu_id_1)
        id_2 = bin(app_id << 16 | cu_id_2)
        # id_1 = (bin(app_id) << 16) + bin(cu_id_1)
        # id_2 = (bin(app_id) << 16) + bin(cu_id_2)
        print("id_1 binary:", id_1)
        print("id_2 binary:", id_2)

        id_1_int = int(id_1, 2)
        id_2_int = int(id_2, 2)
        print("id_1 int:", id_1_int)
        print("id_2 int:", id_2_int)

        id_1_sep_app = bin(id_1_int >> 16)
        id_1_sep_cu = bin(id_1_int & 0b1111111111111111)
        id_2_sep_app = bin(id_1_int >> 16)
        id_2_sep_cu = bin(id_2_int & 0b1111111111111111)

        print("id_1_sep_app:", id_1_sep_app)
        print("id_1_sep_cu:", id_1_sep_cu)
        print("id_2_sep_app:", id_2_sep_app)
        print("id_2_sep_cu:", id_2_sep_cu)


if __name__ == '__main__':
    unittest.main()
