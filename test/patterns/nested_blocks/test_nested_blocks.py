# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
        self.assertEqual(lines, [15, 19])

    def test_nested_for_loops(self):
        filepath = self.current_directory / "NestedFor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [22])

    def test_for_loops_in_different_methods(self):
        filepath = self.current_directory / "DifferentMethods.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [28])

    def test_for_loops_in_nested_class(self):
        filepath = self.current_directory / "NestedForInNestedClasses.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [9])

    def test_for_loops_in_anonymous_class(self):
        filepath = self.current_directory / "ForInAnonymousFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NestedBlocks(2, ASTNodeType.FOR_STATEMENT)
        lines = pattern.value(ast)
        self.assertEqual(lines, [19])

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
        self.assertEqual(lines, [21, 42])
