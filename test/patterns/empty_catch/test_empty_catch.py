# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.empty_catch.empty_catch import EmptyCatch
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class EmptyCatchPatternTestCase(TestCase):
    """
    Test cases for the P36 (Empty Catch Block) pattern.
    """
    current_directory = Path(__file__).absolute().parent

    def test_empty(self):
        """
        Verify that an empty catch block is detected.
        The parser returns the line of the 'try' keyword (line 6).
        """
        filepath = self.current_directory / 'Empty.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyCatch()
        lines = pattern.value(ast)
        self.assertEqual(lines, [6])

    def test_not_empty(self):
        """
        Verify that a catch block with statements is ignored.
        """
        filepath = self.current_directory / 'NotEmpty.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyCatch()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_no_catch(self):
        """
        Verify that a try-finally block without a catch clause is ignored.
        """
        filepath = self.current_directory / 'NoCatch.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyCatch()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
