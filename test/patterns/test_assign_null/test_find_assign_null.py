# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from aibolit.ast_framework.ast import AST
from aibolit.patterns.assign_null_finder.assign_null_finder import NullAssignment
from aibolit.utils.ast_builder import build_ast


class NullAssignmentTestCase(TestCase):
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    def test_several(self):
        test_file = os.path.join(self.cur_dir, 'several.java')
        ast = AST.build_from_javalang(build_ast(test_file))
        lines = NullAssignment().value(ast)
        self.assertEqual(lines, [8, 9, 14, 18, 24, 25])

    def test_one(self):
        test_file = os.path.join(self.cur_dir, 'one.java')
        ast = AST.build_from_javalang(build_ast(test_file))
        lines = NullAssignment().value(ast)
        self.assertEqual(lines, [11])

    def test_not_null(self):
        test_file = os.path.join(self.cur_dir, 'not_null.java')
        ast = AST.build_from_javalang(build_ast(test_file))
        lines = NullAssignment().value(ast)
        self.assertEqual(lines, [])
