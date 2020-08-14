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

from aibolit.patterns.array_as_argument.array_as_argument import ArrayAsArgument
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ArrayAsArgumentTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    pattern = ArrayAsArgument()

    def test_NoArgument(self):
        file = Path(self.dir_path, "NoArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([], self.pattern.value(ast), "Should not match no argument method")

    def test_PrimitiveAsArgument(self):
        file = Path(self.dir_path, "PrimitiveAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([], self.pattern.value(ast), "Should not match method with primitive as argument")

    def test_ArrayAsArgument(self):
        file = Path(self.dir_path, "ArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([2], self.pattern.value(ast), "Should match method with array as argument")

    def test_ObjectAsArgument(self):
        file = Path(self.dir_path, "ObjectAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([], self.pattern.value(ast), "Should not match method with object as argument")

    def test_PrimitiveAndArrayAsArgument(self):
        file = Path(self.dir_path, "PrimitiveAndArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([2], self.pattern.value(ast), "Should match method with array as argument")

    def test_GenericArrayAsArgument(self):
        file = Path(self.dir_path, "GenericArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([2], self.pattern.value(ast), "Should match method with generic array as argument")

    def test_ConstructorWithArrayAsArgument(self):
        file = Path(self.dir_path, "ConstructorWithArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([2], self.pattern.value(ast), "Should match constructor with array as argument")
