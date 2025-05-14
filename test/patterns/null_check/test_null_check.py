# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.null_check.null_check import NullCheck
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class NullCheckTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_null_check(self):
        filepath = self.current_directory / "1.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_null_check_in_constructor(self):
        filepath = self.current_directory / "2.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_null_check_comparison_result_assignment(self):
        filepath = self.current_directory / "3.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_null_check_ternary(self):
        filepath = self.current_directory / "4.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_null_check_not_equal_comparison(self):
        filepath = self.current_directory / "5.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])
