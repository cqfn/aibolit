# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path

from aibolit.patterns.implements_multi.implements_multi import ImplementsMultiFinder
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ImplementsMultiTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_one_class_with_types(self):
        filepath = self.current_directory / "AnimatableSplitDimensionPathValue.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_two_classes(self):
        filepath = self.current_directory / "AnimatableTransform.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])

    def test_implements_in_string(self):
        filepath = self.current_directory / "AuditEventModelProcessor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_implements_with_parantheses(self):
        filepath = self.current_directory / "BaseKeyframeAnimation.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_implements_with_nested_parantheses(self):
        filepath = self.current_directory / "Configuration.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [228])

    def test_implements_multi_classes(self):
        filepath = self.current_directory / "FillContent.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [32])

    def test_implements_with_parantheses_multi(self):
        filepath = self.current_directory / "FJIterateTest.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [597])

    def test_implements_with_parantheses_before(self):
        filepath = self.current_directory / "FJListProcedureRunner.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_implements_in_comments(self):
        filepath = self.current_directory / "KeyProviderCryptoExtension.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_implements_multi(self):
        filepath = self.current_directory / "OsSecureRandom.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [45])

    def test_implements_three(self):
        filepath = self.current_directory / "RectangleContent.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [25])

    def test_implements_many(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [840])
