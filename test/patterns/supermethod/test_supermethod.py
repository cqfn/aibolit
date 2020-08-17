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
