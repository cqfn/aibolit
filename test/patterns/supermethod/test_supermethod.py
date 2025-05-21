# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.supermethod.supermethod import SuperMethod
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class SuperMethodTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_empty(self):
        filepath = self.current_directory / "Empty.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SuperMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 0)

    def test_instance_of(self):
        # It has 2 matches in anonymous class!
        filepath = self.current_directory / "Anonymous.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SuperMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 1)

    def test_instance(self):
        filepath = self.current_directory / "Simple.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SuperMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 1)

    def test_several(self):
        # It has 2 matches in anonymous class!
        filepath = self.current_directory / "Several.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SuperMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 6)

    def test_nested_class(self):
        filepath = self.current_directory / "NestedClass.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SuperMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 1)

    def test_constructor(self):
        filepath = self.current_directory / "Constructor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SuperMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 3)

    def test_complicated_constructor(self):
        filepath = self.current_directory / "ComplicatedChainConstructor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SuperMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 0)
