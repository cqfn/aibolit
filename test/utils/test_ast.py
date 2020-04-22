import os
from unittest import TestCase
from pathlib import Path
from aibolit.utils.ast import AST


class TestAST(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_wrong_file(self):
        self.assertRaises(
            TypeError,
            AST(Path(self.dir_path, 'test_ast.py')).value
        )
