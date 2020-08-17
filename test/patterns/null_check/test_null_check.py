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

from aibolit.patterns.null_check.null_check import NullCheck
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class NullCheckTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_null_check(self):
        filepath = self.current_directory / "1.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [4])

    def test_null_check_in_constructor(self):
        filepath = self.current_directory / "2.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_null_check_comparison_result_assignment(self):
        filepath = self.current_directory / "3.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [4])

    def test_null_check_ternary(self):
        filepath = self.current_directory / "4.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [4])

    def test_null_check_not_equal_comparison(self):
        filepath = self.current_directory / "5.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NullCheck()
        lines = pattern.value(ast)
        self.assertEqual(lines, [4])
