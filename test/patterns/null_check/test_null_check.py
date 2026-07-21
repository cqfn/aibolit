# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.null_check.null_check import NullCheck
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class NullCheckTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_null_check(self):
        """Verify detection of a standard null check using '=='."""
        filepath = self.current_directory / '1.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_null_check_in_constructor(self):
        """Verify that null checks inside constructors are correctly excluded."""
        filepath = self.current_directory / '2.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_null_check_comparison_result_assignment(self):
        """Verify detection of null check assigned to a boolean variable."""
        filepath = self.current_directory / '3.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_null_check_ternary(self):
        """Verify detection of null check inside a ternary operator."""
        filepath = self.current_directory / '4.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_null_check_not_equal_comparison(self):
        """Verify detection of a standard null check using '!='."""
        filepath = self.current_directory / '5.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_null_check_in_lambda(self):
        """Verify that P13 correctly handles null checks inside Java Lambda expressions."""
        filepath = self.current_directory / '6.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
