# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class NestedBlocksTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_single_for_loop(self):
        filepath = self.current_directory / "SingleFor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [18, 22])

    def test_nested_for_loops(self):
        filepath = self.current_directory / "NestedFor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [25])

    def test_for_loops_in_different_methods(self):
        filepath = self.current_directory / "DifferentMethods.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [31])

    def test_for_loops_in_nested_class(self):
        filepath = self.current_directory / "NestedForInNestedClasses.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [12])

    def test_for_loops_in_anonymous_class(self):
        filepath = self.current_directory / "ForInAnonymousFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [22])

    def test_nested_no_nested_if(self):
        filepath = self.current_directory / "NestedNoIF.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.IF_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_nested_if(self):
        filepath = self.current_directory / "NestedIF.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.IF_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [24, 45])
