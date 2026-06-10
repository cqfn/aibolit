# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
from unittest import TestCase

from aibolit.utils.utils import RemoveComments


class TestRemoveComments(TestCase):

    def test_preserves_double_slash_inside_string_literal(self):
        source = (
            'class A {\n'
            '    String url = "http://example.com";\n'
            '    int x;\n'
            '}\n'
        )

        self.assertEqual(RemoveComments.remove_comments(source), source)

    def test_preserves_literal_content_while_removing_real_comments(self):
        source = (
            'class A {\n'
            '    String text = "/* tag */"; // trailing comment\n'
            "    char slash = '/'; /* block\n"
            '    comment */\n'
            '}\n'
        )
        expected = (
            'class A {\n'
            '    String text = "/* tag */";\n'
            "    char slash = '/';\n"
            '\n'
            '}\n'
        )

        self.assertEqual(RemoveComments.remove_comments(source), expected)
