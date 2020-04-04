# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from unittest import TestCase

from javalang.parser import Parser
from javalang.tokenizer import tokenize

from aibolit.patterns.null_check.null_check import NullCheck


class TestNullCheck(TestCase):
    def setUp(self):
        self.pattern = NullCheck()

    def test_null_check(self):
        snippet = """\
        if (this.z == null) { // here!
            throw new RuntimeException("oops");
        }
        """

        self.assertEqual(
            self.pattern._traverse_node(_parser(snippet).parse_block_statement()), [1]
        )

    def test_null_check_in_constructor(self):
        snippet = """\
        public NullCheck(String z) {
            if (z == null) { // here!
                throw new RuntimeException("oops");
            }
        }
        """

        self.assertEqual(
            self.pattern._traverse_node(_parser(snippet).parse_member_declaration()),
            [],
        )

    def test_null_check_comparison_result_assignment(self):
        snippet = "boolean i = z == null;"

        self.assertEqual(
            self.pattern._traverse_node(_parser(snippet).parse_block_statement()), [1]
        )

    def test_null_check_ternary(self):
        snippet = 'luckyName == null ? luckyName : "No lucky name found";'

        self.assertEqual(
            self.pattern._traverse_node(_parser(snippet).parse_block_statement()), [1]
        )

    def test_null_check_not_equal_comparison(self):
        snippet = """\
        if (this.z != null) { // here!
            throw new RuntimeException("oops");
        }
        """

        self.assertEqual(
            self.pattern._traverse_node(_parser(snippet).parse_block_statement()), [1]
        )


def _parser(snippet, debug=False):
    parser = Parser(tokenize(snippet))

    if debug:
        parser.set_debug()

    return parser
