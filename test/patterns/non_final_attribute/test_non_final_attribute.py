# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

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
        self.assertEqual(lines, [5, 7, 9, 11])

    def test_nested_class(self):
        filepath = self.current_directory / "File.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalAttribute()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15, 19, 67])

    def test_attribute_in_interface(self):
        filepath = self.current_directory / "AttributeInInterface.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalAttribute()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
