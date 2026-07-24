# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.empty_finally.empty_finally import EmptyFinally
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class EmptyFinallyPatternTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_empty(self):
        filepath = self.current_directory / 'Empty.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyFinally()
        lines = pattern.value(ast)
        # The number of line depends on the parser.
        self.assertEqual(lines, [6])

    def test_not_empty(self):
        filepath = self.current_directory / 'NotEmpty.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyFinally()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_no_finally(self):
        filepath = self.current_directory / 'NoFinally.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyFinally()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
