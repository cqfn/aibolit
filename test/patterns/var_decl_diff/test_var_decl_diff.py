# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from aibolit.ast_framework.ast import AST
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance
from aibolit.utils.ast_builder import build_ast


class VarDeclarationDiffTestCase(TestCase):
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    def test_good_class(self):
        test_file = os.path.join(self.cur_dir, '1.java')
        ast = AST.build_from_javalang(build_ast(test_file))
        pattern = VarDeclarationDistance(lines_th=2)
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_bad_class(self):
        test_file = os.path.join(self.cur_dir, '2.java')
        ast = AST.build_from_javalang(build_ast(test_file))
        pattern = VarDeclarationDistance(lines_th=2)
        lines = pattern.value(ast)
        self.assertEqual(lines, [16])

    def test_bad_class2(self):
        test_file = os.path.join(self.cur_dir, '3.java')
        ast = AST.build_from_javalang(build_ast(test_file))
        pattern = VarDeclarationDistance(lines_th=5)
        lines = pattern.value(ast)
        self.assertEqual(sorted(lines), [216, 785, 971])

    def test_case_with_multiline_function_arguments(self):
        test_file = os.path.join(self.cur_dir, '4.java')
        ast = AST.build_from_javalang(build_ast(test_file))
        pattern = VarDeclarationDistance(lines_th=2)
        lines = pattern.value(ast)
        self.assertEqual(lines, [17, 21])
