# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
import unittest

from aibolit.patterns.method_siblings.method_siblings import MethodSiblings
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class MethodSiblingsTestCase(unittest.TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_find_simple_method_siblings(self):
        filepath = self.current_directory / "SimpleMethodSiblings.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodSiblings()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5, 8])

    def test_find_alternate_method_siblings(self):
        filepath = self.current_directory / "AlternateMethodSiblings.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodSiblings()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5, 11])
