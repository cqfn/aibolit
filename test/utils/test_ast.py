import os
from unittest import TestCase
from pathlib import Path
from aibolit.utils.ast import AST


class TestAST(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_open_file(self):
        ast = AST(Path(self.dir_path, 'ConditionalExpressionCheck.java'))
        ast.value()
        self.assertEqual(ast.encoding, 'UTF-8')

    def test_utf(self):
        ast = AST(Path(self.dir_path, 'ExceptionDemo.java'))
        ast.value()
        self.assertEqual(ast.encoding, 'GB18030')
