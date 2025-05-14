# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.public_static_method.public_static_method import PublicStaticMethod
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class PublicStaticMethodPatternTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_find_non_final_attributes(self):
        filepath = self.current_directory / "PublicStaticMethod.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = PublicStaticMethod()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 1)
