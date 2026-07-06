# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent
from unittest import TestCase

from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast_from_string


class AssertInCodeTestCase(TestCase):
    def test_assert_in_code(self):
        content = dedent(
            '''\
            class Book {
              void foo(String x) {
                assert x != null; // here
              }
            }
            '''
        )
        ast = AST.build_from_javalang(build_ast_from_string(content))
        self.assertEqual(AssertInCode().value(ast), [3])
