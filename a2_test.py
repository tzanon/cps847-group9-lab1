import unittest
from a2 import area

class A2Test(unittest.TestCase):
    def test_area(self):
        self.assertAlmostEqual(area(2,5), 10)
        self.assertAlmostEqual(area(0,5), 0)

    def test_validity(self):
        self.assertRaises(ValueError, area, 'lol', -5)
        self.assertRaises(ValueError, area, -2, 'wow')