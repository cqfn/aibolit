# SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path

from aibolit.patterns.method_chaining.method_chaining import MethodChainFind
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class MethodChainTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_method_chain(self):
        filepath = self.current_directory / "MethodChain.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [21])

    def test_empty_method_chain(self):
        filepath = self.current_directory / "EmptyMethodChain.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [21])

    def test_chain_with_new_object(self):
        filepath = self.current_directory / "MethodChainNewObjectMethods.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [23, 34])

    def test_method_chain_in_different_methods(self):
        filepath = self.current_directory / "MethodChainInDifferentMethods.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [22, 34])

    def test_chain_in_nested_class(self):
        filepath = self.current_directory / "MethodChainNestedClass.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [19])

    def test_chain_in_anonymous_class(self):
        filepath = self.current_directory / "MethodChainAnonymousClass.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [29])

    def test_chain_in_anonymous_class_empty(self):
        filepath = self.current_directory / "MethodChainAnonymousClassEmpty.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_several_chains(self):
        filepath = self.current_directory / "MethodChainSeveral.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [13, 34, 48])

    def test_chain_without_object_creating(self):
        filepath = self.current_directory / "WithoutObjectCreating.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [14])

    def test_nested_chain_with_this(self):
        filepath = self.current_directory / "NestedChainWIthThis.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [14, 15])

    def test_nested_chain_with_simple_method_invocation(self):
        filepath = self.current_directory / "NestedChainWithSimpleMethodInvocation.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15, 16])

    def test_nested_chain_complicated_structure(self):
        """
        Several nested structures are checked: nested method chaining
        with nested anonymous classes
        """
        filepath = self.current_directory / "HolyMolyNestedChain.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [60, 67, 77])

    def test_smallest_chain(self):
        filepath = self.current_directory / "SmallestChain.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [31, 83, 84])

    def test_fake_chain(self):
        filepath = self.current_directory / "FakeChain.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_many_chains(self):
        filepath = self.current_directory / "MachineLearningGetResultsIT.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MethodChainFind()
        lines = pattern.value(ast)
        self.assertGreater(len(lines), 300)
