# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.multiple_while.multiple_while import MultipleWhile
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class MultipleWhilePatternTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_simple(self):
        filepath = self.current_directory / "Simple.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleWhile()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])

    def test_one_while(self):
        filepath = self.current_directory / "OneWhile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleWhile()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_if_while(self):
        filepath = self.current_directory / "IfWhile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleWhile()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])

    def test_multiple_while(self):
        filepath = self.current_directory / "MultipleWhile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleWhile()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
