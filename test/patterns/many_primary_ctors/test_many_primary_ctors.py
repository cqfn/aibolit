# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.many_primary_ctors.many_primary_ctors import ManyPrimaryCtors
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ManyPrimaryCtorsTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_many_primary_ctors(self):
        filepath = self.current_directory / "Book.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ManyPrimaryCtors()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7, 11])
