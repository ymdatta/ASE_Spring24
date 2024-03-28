import sys
sys.path.append("../src")
from src.NUM import NUM
import unittest

class NumTestSuite(unittest.TestCase):
    def test_add(self):
        num = NUM()
        num.add(5)
        self.assertEqual(num.n, 1)
        self.assertEqual(num.mu, 5)
        self.assertEqual(num.m2, 0)
        self.assertEqual(num.lo, 5)
        self.assertEqual(num.hi, 5)

    def test_mid(self):
        num = NUM()
        num.add(5)
        num.add(7)
        self.assertEqual(num.mid(), 6)

    def test_div(self):
        num = NUM()
        num.add(5)
        num.add(7)
        self.assertEqual(num.div(), 1.4142135623730951)

    def test_small(self):
        num = NUM()
        num.add(5)
        num.add(7)
        self.assertEqual(num.small(), 0.4949489742783178)

if __name__ == '__main__':
    unittest.main()