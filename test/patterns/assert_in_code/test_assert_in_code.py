# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode
from aibolit.utils.ast_builder import build_ast_from_string


def book_content() -> str:
    return dedent(
        '''\
        // SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
        // SPDX-License-Identifier: MIT

        class Book {
          void foo(String x) {
            assert x != null; // here
          }
        }
        '''
    )


class AssertInCodeTestCase(TestCase):

    def test_assert_in_code(self):
        ast = AST.build_from_javalang(build_ast_from_string(book_content()))
        self.assertEqual(AssertInCode().value(ast), [6])
