# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from pathlib import Path

from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ConcatStringTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_concat_strings_in_print(self):
        filepath = Path(self.dir_path, "ConcatInPrint.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [17])

    def test_member_plus_string(self):
        filepath = Path(self.dir_path, "MemberPlusString.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [101, 113])

    def test_empty_case(self):
        filepath = Path(self.dir_path, "Nothing.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_string_plus_member(self):
        filepath = Path(self.dir_path, "StringPlusMember.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(len(lines), 1)

    def test_many_concats(self):
        filepath = Path(self.dir_path, "ManyConcats.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15, 16, 17, 18])

    def test_concat_in_different_methods(self):
        filepath = Path(self.dir_path, "DifferentMethods.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [16, 30])

    def test_fake_operator_plus(self):
        filepath = Path(self.dir_path, "FakePlusOperator.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_string_with_quotes(self):
        filepath = Path(self.dir_path, "RustServerCodegen.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(
            lines,
            [
                354,
                374,
                375,
                381,
                382,
                410,
                411,
                420,
                424,
                431,
                432,
                440,
                458,
                468,
                481,
                496,
                501,
                511,
                564,
                565,
                606,
                607,
                612,
                703,
                997,
                1011,
                1014,
                1031,
                1034,
                1082,
                1190,
                1260,
                1269,
                1339,
                1368,
                1374,
                1388,
                1416,
            ],
        )

    def test_comment_inside_line(self):
        filepath = Path(self.dir_path, "XMLDataObject.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [162, 167, 179, 194, 220, 281])

    def test_fake1(self):
        filepath = Path(self.dir_path, "Chain.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [34])
