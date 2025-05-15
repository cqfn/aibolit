# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

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
        self.assertEqual(
            [], self.pattern.value(ast), "Should not match method with primitive as argument"
        )

    def test_ArrayAsArgument(self):
        file = Path(self.dir_path, "ArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([5], self.pattern.value(ast), "Should match method with array as argument")

    def test_ObjectAsArgument(self):
        file = Path(self.dir_path, "ObjectAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual(
            [], self.pattern.value(ast), "Should not match method with object as argument"
        )

    def test_PrimitiveAndArrayAsArgument(self):
        file = Path(self.dir_path, "PrimitiveAndArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual([5], self.pattern.value(ast), "Should match method with array as argument")

    def test_GenericArrayAsArgument(self):
        file = Path(self.dir_path, "GenericArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual(
            [5], self.pattern.value(ast), "Should match method with generic array as argument"
        )

    def test_ConstructorWithArrayAsArgument(self):
        file = Path(self.dir_path, "ConstructorWithArrayAsArgument.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual(
            [5], self.pattern.value(ast), "Should match constructor with array as argument"
        )
