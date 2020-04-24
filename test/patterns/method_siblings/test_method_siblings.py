import os
import unittest
from aibolit.patterns.method_siblings.method_siblings import MethodSiblings
from pathlib import Path


class TestMethodSiblingsSiblings(unittest.TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    @unittest.skip("Not implemented")
    def test_find_simple_method_siblings(self):
        self.assertEqual(
            [2], MethodSiblings(Path(self.dir_path, 'SimpleMethodSiblings.java')).value()
        )

    @unittest.skip("Not implemented")
    def test_find_alternate_method_siblings(self):
        self.assertEqual(
            [2], MethodSiblings(Path(self.dir_path, 'AlternateMethodSiblings.java')).value()
        )
