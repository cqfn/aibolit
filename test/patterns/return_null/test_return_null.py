# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.return_null.return_null import ReturnNull
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ReturnNullPatternTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_anonymous(self):
        filepath = self.current_directory / "Anonymous.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [27, 31])

    def test_empty(self):
        filepath = self.current_directory / "Empty.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_with_ternary1(self):
        filepath = self.current_directory / "With_Ternary1.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])

    def test_with_ternary2(self):
        filepath = self.current_directory / "With_Ternary2.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])

    def test_with_ternary_not_return_null(self):
        filepath = self.current_directory / "With_Ternary_not_return_null.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple(self):
        filepath = self.current_directory / "Simple.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])
