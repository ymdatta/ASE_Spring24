import sys
sys.path.append("../src")
from src.ROW import ROW
import unittest

class RowTestSuite:
    def test_init(self):
        t = ['8', '304', '193', '70', '1', '4732', '18.5', '10']
        assert row.cells == {1:'8',2:'304',3:'193',4:'70',5:'1',6:'4732',7:'18.5',8:'10'}

if __name__ == '__main__':
    unittest.main()