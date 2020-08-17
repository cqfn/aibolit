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

from aibolit.patterns.non_final_class.non_final_class import NonFinalClass
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class NonFinalClassTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_find_final_class(self):
        filepath = self.current_directory / "1.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_find_non_final_class(self):
        filepath = self.current_directory / "2.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [1])

    def test_abstract_class(self):
        filepath = self.current_directory / "3.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
