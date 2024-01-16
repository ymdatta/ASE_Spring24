import unittest
import sys
sys.path.append("../src")
from src.SYM import SYM

class SymTestSuite(unittest.TestCase):
    def setUp(self):
        self.sym = SYM()

    def test_add(self):
        self.sym.add("a")
        self.assertEqual(self.sym.n, 1)
        self.assertEqual(self.sym.has["a"], 1)
        self.assertEqual(self.sym.mode, "a")
        self.assertEqual(self.sym.most, 1)

    def test_mid(self):
        self.sym.add("a")
        self.assertEqual(self.sym.mid(), "a")

    def test_div(self):
        self.sym.add("a")
        self.sym.add("b")
        self.assertAlmostEqual(self.sym.div(0), 1.0)  # Replace 0 with the actual value of e

    def test_small(self):
        self.assertEqual(self.sym.small(0), 0)  # Replace 0 with the actual value of _

if __name__ == '__main__':
    unittest.main()