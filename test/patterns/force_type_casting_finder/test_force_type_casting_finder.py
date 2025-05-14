# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase

from aibolit.patterns.force_type_casting_finder import force_type_casting_finder
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ForceTypeCastingFinderTestCase(TestCase):
    def test_simple(self):
        pattern = force_type_casting_finder.ForceTypeCastingFinder()
        path = os.path.dirname(os.path.realpath(__file__)) + "/1.java"
        ast = AST.build_from_javalang(build_ast(path))
        lines = pattern.value(ast)
        self.assertEqual(lines, [8])

    def test_several_casts(self):
        pattern = force_type_casting_finder.ForceTypeCastingFinder()
        path = os.path.dirname(os.path.realpath(__file__)) + "/2.java"
        ast = AST.build_from_javalang(build_ast(path))
        lines = pattern.value(ast)
        self.assertEqual(lines, [8, 14, 20])

    def test_zero_lines(self):
        pattern = force_type_casting_finder.ForceTypeCastingFinder()
        path = os.path.dirname(os.path.realpath(__file__)) + "/3.java"
        ast = AST.build_from_javalang(build_ast(path))
        lines = pattern.value(ast)
        self.assertEqual(lines, [])
