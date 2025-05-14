# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance


class VarDeclarationDiffTestCase(TestCase):
    def test_good_class(self):
        pattern = VarDeclarationDistance(lines_th=2)
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + "/1.java")
        self.assertEqual(lines, [])

    def test_bad_class(self):
        pattern = VarDeclarationDistance(lines_th=2)
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + "/2.java")
        self.assertEqual(lines, [16])

    def test_bad_class2(self):
        pattern = VarDeclarationDistance(lines_th=5)
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + "/3.java")
        self.assertEqual(sorted(lines), [216, 785, 971])

    def test_case_with_multiline_function_arguments(self):
        pattern = VarDeclarationDistance(lines_th=2)
        lines = pattern.value(os.path.dirname(os.path.realpath(__file__)) + "/4.java")
        self.assertEqual(lines, [17, 21])
