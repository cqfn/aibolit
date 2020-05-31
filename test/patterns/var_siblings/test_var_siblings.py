import os
import unittest
from aibolit.patterns.var_siblings.var_siblings import VarSiblings
from pathlib import Path


class TestVarSiblings(unittest.TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_simple_var_siblings(self):
        self.assertEqual(
            [3, 4], VarSiblings().value(Path(self.dir_path, 'SimpleVarSiblings.java'))
        )

    def test_find_alternate_var_siblings(self):
        self.assertEqual(
            [3, 5], VarSiblings().value(Path(self.dir_path, 'AlternateVarSiblings.java'))
        )

    def test_find_length_4_var_siblings(self):
        self.assertEqual(
            [9, 10], VarSiblings().value(Path(self.dir_path, 'ShortVarSiblings.java'))
        )
