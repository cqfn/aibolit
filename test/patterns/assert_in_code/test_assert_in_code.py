# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os.path
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class AssertInCodeTestCase(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent

    def test_assert_in_code(self):
        file = Path(self.cur_file_dir, "Book.java")
        ast = AST.build_from_javalang(build_ast(file))
        self.assertEqual(AssertInCode().value(ast), [6])
