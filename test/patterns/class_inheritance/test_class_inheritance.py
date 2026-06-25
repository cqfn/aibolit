# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.patterns.class_inheritance.class_inheritance import ClassInheritance
from aibolit.utils.ast_builder import build_ast


class ClassInheritanceTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_find_class_inheritance(self):
        filepath = self.current_directory / 'SimpleInheritance.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassInheritance()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7])

    def test_ignore_implements_only(self):
        filepath = self.current_directory / 'OnlyImplements.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassInheritance()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_ignore_type_parameter_extends(self):
        filepath = self.current_directory / 'TypeParameterExtends.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassInheritance()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_find_nested_class_inheritance(self):
        filepath = self.current_directory / 'NestedInheritance.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassInheritance()
        lines = pattern.value(ast)
        self.assertEqual(lines, [10])
