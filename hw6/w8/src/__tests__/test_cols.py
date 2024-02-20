import unittest
import sys
sys.path.append("../src")
from src.COLS import COLS

class ColsTestSuite(unittest.TestCase):
    def setUp(self):
        self.row = ['8', '304', '193', '70', '1', '4732', '18.5', '10']
        self.row.cells = {1: '8', 2: '304', 3: '193', 4: '70', 5: '1', 6: '4732', 7:'18.5', 8:'10'}

    def test_init(self):
        cols = COLS(self.row)
        self.assertEqual(cols.names, self.row.cells)

    def test_add(self):
        cols = COLS(self.row)
        new_row = ['8', '360', '215', '70', '1', '4615', '14', '10']
        new_row.cells = {1: '8', 2: '360', 3: '215', 4: '70', 5: '1', 6: '4615', 7:'14', 8:'10'}
        updated_row = cols.add(new_row)
        self.assertEquals(updated_row, new_row.cells)

if __name__ == '__main__':
    unittest.main()