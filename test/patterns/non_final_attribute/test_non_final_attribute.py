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

from aibolit.patterns.non_final_attribute.non_final_attribute import NonFinalAttribute
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class NonFinalAttributeTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_find_non_final_attributes(self):
        filepath = self.current_directory / "NonFinalAttribute.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalAttribute()
        lines = pattern.value(ast)
        self.assertEqual(lines, [2, 4, 6, 8])

    def test_nested_class(self):
        filepath = self.current_directory / "File.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalAttribute()
        lines = pattern.value(ast)
        self.assertEqual(lines, [12, 16, 64])

    def test_attribute_in_interface(self):
        filepath = self.current_directory / "AttributeInInterface.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalAttribute()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
