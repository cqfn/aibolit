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

import os
from unittest import TestCase
from pathlib import Path

from aibolit.patterns.if_return_if_detection.if_detection import CountIfReturn
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class CountIfReturnTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_2nd_level_inside(self):
        filepath = Path(self.dir_path, "1.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [6, 10])

    def test_no_return_inside(self):
        filepath = Path(self.dir_path, "2.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_nested_one_goodreturn(self):
        filepath = Path(self.dir_path, "3.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_nested_one_badreturn(self):
        filepath = Path(self.dir_path, "4.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [6])

    def test_withandwithout_returns(self):
        filepath = Path(self.dir_path, "5.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [6, 14, 16, 18])

    def test_nomoreReturn_and_nested(self):
        filepath = Path(self.dir_path, "6.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [10])
