import unittest
from autoslicer import AutoSlicer

class TestAutoSlicer(unittest.TestCase):
    def setUp(self):
        self.slicer = AutoSlicer("TestWorkspace")

    def test_set_threshold(self):
        self.slicer.set_threshold(-100, 200)
        self.assertEqual(self.slicer.lower_, -100)
        self.assertEqual(self.slicer.upper_, 200)

    def test_set_density(self):
        initial_density = self.slicer.lower_
        self.slicer.set_density(100, 1.08)
        self.assertEqual(initial_density, -96.25)  
        self.slicer.set_density(200, 0.95)