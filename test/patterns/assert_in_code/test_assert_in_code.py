# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode


def book_content() -> str:
    return dedent(
        '''\
        // SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
        // SPDX-License-Identifier: MIT

        class Book {
          void foo(String x) {
            assert x != null;
          }
        }
        '''
    )


class AssertInCodeTestCase(TestCase):

    def test_assert_in_code(self):
        ast = AST.from_string(book_content())
        self.assertEqual(AssertInCode().value(ast), [6])
