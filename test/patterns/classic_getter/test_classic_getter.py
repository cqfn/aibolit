# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.classic_getter.classic_getter import ClassicGetter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class SetterTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_no_getters(self):
        filepath = self.current_directory / "NoGetters.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_fake_getter(self):
        filepath = self.current_directory / "FakeGetter.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_long_fake_getter(self):
        filepath = self.current_directory / "LongFake.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple(self):
        filepath = self.current_directory / "SimpleGetter.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [8])
