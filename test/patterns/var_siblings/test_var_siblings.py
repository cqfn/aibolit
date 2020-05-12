import os
import unittest
from aibolit.patterns.var_siblings.var_siblings import VarSiblings
from pathlib import Path


class TestVarSiblings(unittest.TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    @unittest.skip("Not implemented")
    def test_find_simple_var_siblings(self):
        self.assertEqual(
            [(3, 4)], VarSiblings(Path(self.dir_path, 'SimpleVarSiblings.java')).value()
        )

    @unittest.skip("Not implemented")
    def test_find_alternate_var_siblings(self):
        self.assertEqual(
            [(3, 5)], VarSiblings(Path(self.dir_path, 'AlternateVarSiblings.java')).value()
        )
