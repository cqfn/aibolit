import unittest
from aibolit.metrics.mda.mda import MDAMetric
from pathlib import Path
import os


class TestMDAMetric(unittest.TestCase):
    mda_metric = MDAMetric()
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_book(self):

        file = Path(self.dir_path, 'Book.java')
        result = self.mda_metric.value(file)
        self.assertEqual(result, 6)

    def test_one(self):

        file = Path(self.dir_path, 'FirstTest.java')
        result = self.mda_metric.value(file)
        self.assertEqual(result, 8)

    def test_two(self):

        file = Path(self.dir_path, 'SecondTest.java')
        result = self.mda_metric.value(file)
        self.assertEqual(result, 7)

    def test_three(self):

        file = Path(self.dir_path, 'ThirdTest.java')
        result = self.mda_metric.value(file)
        self.assertEqual(result, 9)
