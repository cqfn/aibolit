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
        self.assertEqual(lines, [12])

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
        self.assertEqual(lines, [225])

    def test_implements_multi_classes(self):
        filepath = self.current_directory / "FillContent.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [29])

    def test_implements_with_parantheses_multi(self):
        filepath = self.current_directory / "FJIterateTest.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [601])

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
        self.assertEqual(lines, [42])

    def test_implements_three(self):
        filepath = self.current_directory / "RectangleContent.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [22])

    def test_implements_many(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ImplementsMultiFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [837])
