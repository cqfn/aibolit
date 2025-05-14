# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.multiple_try.multiple_try import MultipleTry
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class MultipleTryPatternTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_simple(self):
        filepath = self.current_directory / "Simple.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])

    def test_large_file(self):
        filepath = self.current_directory / "Large.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [622, 708])

    def test_try_inside_anonymous(self):
        filepath = self.current_directory / "TryInsideAnomymous.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [8])

    def test_try_inside_catch(self):
        filepath = self.current_directory / "TryInsideCatch.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])

    def test_try_inside_finally(self):
        filepath = self.current_directory / "TryInsideFinaly.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])

    def test_try_inside_try(self):
        filepath = self.current_directory / "TryInsideTry.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])

    def test_try_method_overloading(self):
        filepath = self.current_directory / "TryMethodOverloading.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
