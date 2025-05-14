# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.instanceof.instance_of import InstanceOf
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class InstanceOfTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_empty(self):
        filepath = self.current_directory / "Empty.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 0)

    def test_instance_of(self):
        filepath = self.current_directory / "InstanceOfSample.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 1)

    def test_instance(self):
        filepath = self.current_directory / "InstanceSample.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 1)

    def test_instance_of_different_methods(self):
        filepath = self.current_directory / "InstanceOfSampleDifferentMethods.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 2)

    def test_instance_different_methods(self):
        filepath = self.current_directory / "InstanceSampleDifferentMethods.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 2)

    def test_instance_of_several(self):
        filepath = self.current_directory / "InstanceOfSampleSeveral.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 3)

    def test_instance_several(self):
        filepath = self.current_directory / "InstanceSampleSeveral.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 2)

    def test_instance_in_method_chaining(self):
        filepath = self.current_directory / "InstanceSampleChain.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 2)

    def test_both(self):
        filepath = self.current_directory / "InstanceBoth.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = InstanceOf()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 2)
