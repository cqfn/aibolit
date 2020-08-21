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

from aibolit.metrics.cognitiveC.cognitive_c import CognitiveComplexity
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class CognitiveComplexityTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test1(self):
        filepath = self.current_directory / '1.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 7)

    def test2(self):
        filepath = self.current_directory / '2.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 9)

    def test3(self):
        filepath = self.current_directory / '3.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 10)

    def test4(self):
        filepath = self.current_directory / '4.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 6)

    def test5(self):
        filepath = self.current_directory / '5.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 3)

    def test6(self):
        filepath = self.current_directory / '6.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 14)

    def test7(self):
        filepath = self.current_directory / 'recursion.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 6)

    def test8(self):
        filepath = self.current_directory / 'nested.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 9)

    def test9(self):
        filepath = self.current_directory / '7.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 17)

    def test10(self):
        filepath = self.current_directory / '8.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 13)
