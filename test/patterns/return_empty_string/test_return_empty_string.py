# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.return_empty_string.return_empty_string import ReturnEmptyString
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ReturnEmptyStringPatternTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_simple(self):
        filepath = self.current_directory / 'Simple.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnEmptyString()
        lines = pattern.value(ast)
        # В файле Simple.java return "" на 3-й строке
        self.assertEqual(lines, [3])

    def test_not_empty(self):
        filepath = self.current_directory / 'NotEmpty.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnEmptyString()
        lines = pattern.value(ast)
        # В файле NotEmpty.java нет пустых строк
        self.assertEqual(lines, [])

    def test_multiple(self):
        filepath = self.current_directory / 'Multiple.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ReturnEmptyString()
        lines = pattern.value(ast)
        # В файле Multiple.java return "" на 3-й и 11-й строках
        self.assertEqual(lines, [3, 12])
