# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
import unittest

from aibolit.patterns.var_siblings.var_siblings import VarSiblings
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class VarSiblingsTestCase(unittest.TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_find_simple_var_siblings(self):
        filepath = self.current_directory / "SimpleVarSiblings.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarSiblings()
        lines = pattern.value(ast)
        self.assertEqual(lines, [6, 7])

    def test_find_alternate_var_siblings(self):
        filepath = self.current_directory / "AlternateVarSiblings.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarSiblings()
        lines = pattern.value(ast)
        self.assertEqual(lines, [6, 8])

    def test_find_length_4_var_siblings(self):
        filepath = self.current_directory / "ShortVarSiblings.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarSiblings()
        lines = pattern.value(ast)
        self.assertEqual(lines, [12, 13])
