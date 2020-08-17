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

from aibolit.patterns.multiple_try.multiple_try import MultipleTry
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class MultipleTryPatternTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_simple(self):
        filepath = self.current_directory / "Simple.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [2])

    def test_large_file(self):
        filepath = self.current_directory / "Large.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [620, 706])

    def test_try_inside_anonymous(self):
        filepath = self.current_directory / "TryInsideAnomymous.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])

    def test_try_inside_catch(self):
        filepath = self.current_directory / "TryInsideCatch.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [2])

    def test_try_inside_finally(self):
        filepath = self.current_directory / "TryInsideFinaly.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [2])

    def test_try_inside_try(self):
        filepath = self.current_directory / "TryInsideTry.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [2])

    def test_try_method_overloading(self):
        filepath = self.current_directory / "TryMethodOverloading.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = MultipleTry()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
