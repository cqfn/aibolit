# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

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
        self.assertEqual(lines, [4])

    def test_abstract_class(self):
        filepath = self.current_directory / "3.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = NonFinalClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
