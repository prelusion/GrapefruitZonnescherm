import unittest


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


if __name__ == '__main__':
    unittest.main()
