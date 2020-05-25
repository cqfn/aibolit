import os
import unittest
from aibolit.patterns.method_siblings.method_siblings import MethodSiblings
from pathlib import Path


class TestMethodSiblingsSiblings(unittest.TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_simple_method_siblings(self):
        self.assertEqual(
            [2, 5], MethodSiblings().value(Path(self.dir_path, 'SimpleMethodSiblings.java'))
        )

    def test_find_alternate_method_siblings(self):
        self.assertEqual(
            [2, 8], MethodSiblings().value(Path(self.dir_path, 'AlternateMethodSiblings.java'))
        )
