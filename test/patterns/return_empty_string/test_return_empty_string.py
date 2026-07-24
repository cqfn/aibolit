# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.return_empty_string.return_empty_string import ReturnEmptyString
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ReturnEmptyStringPatternTestCase(TestCase):
    """
    Test cases for the P33 (Return Empty String) pattern.
    """
    current_directory = Path(__file__).absolute().parent

    def test_simple(self):
        """
        Verify that a simple 'return "";' statement is detected.
        """
        filepath = self.current_directory / 'Simple.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnEmptyString()
        lines = pattern.value(ast)
        # In the file Simple.java, return "" on line 6
        self.assertEqual(lines, [6])

    def test_not_empty(self):
        """
        Verify that a return statement with a normal string is ignored.
        """
        filepath = self.current_directory / 'NotEmpty.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnEmptyString()
        lines = pattern.value(ast)
        # The NotEmpty.java file contains no empty strings.
        self.assertEqual(lines, [])

    def test_multiple(self):
        """
        Verify that multiple empty string returns in one file are all detected.
        """
        filepath = self.current_directory / 'Multiple.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnEmptyString()
        lines = pattern.value(ast)
        # In the Multiple.java file, return "" on lines 6, 15, 20.
        self.assertEqual(lines, [6, 15, 20])
