# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.private_static_method.private_static_method import PrivateStaticMethod
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class PrivateStaticMethodTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_find_private_static_methods(self):
        filepath = self.current_directory / "PrivateStaticMethod.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = PrivateStaticMethod()
        lines = pattern.value(ast)
        self.assertEqual(lines, [5])
