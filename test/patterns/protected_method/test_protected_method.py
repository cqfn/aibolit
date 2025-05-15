# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.protected_method.protected_method import ProtectedMethod
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ProtectedMethodTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_not_find_protected_method(self):
        filepath = self.current_directory / "NoProtectedMethod.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ProtectedMethod()
        lines = pattern.value(ast)
        self.assertEqual(lines, [], "Should not match pattern protected method")

    def test_find_protected_method(self):
        filepath = self.current_directory / "ProtectedMethod.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ProtectedMethod()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5, 9], "Should match pattern protected method")

    def test_find_protected_method_inner(self):
        filepath = self.current_directory / "InnerClassProtectedMethod.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ProtectedMethod()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5, 14], "Should match pattern protected method in inner class")

    def test_find_protected_method_anonymous(self):
        filepath = self.current_directory / "AnonymousClassProtectedMethod.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ProtectedMethod()
        lines = pattern.value(ast)
        self.assertEqual(lines, [8], "Should match pattern protected method in anonymous class")
