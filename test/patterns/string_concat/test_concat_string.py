# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
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
        self.assertEqual(lines, [14])

    def test_member_plus_string(self):
        filepath = Path(self.dir_path, "MemberPlusString.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [99, 111])

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
        self.assertEqual(lines, [12, 13, 14, 15])

    def test_concat_in_different_methods(self):
        filepath = Path(self.dir_path, "DifferentMethods.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [13, 27])

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
                352,
                372,
                373,
                379,
                380,
                408,
                409,
                418,
                422,
                429,
                430,
                438,
                456,
                466,
                479,
                494,
                499,
                509,
                562,
                563,
                604,
                605,
                610,
                701,
                995,
                1009,
                1012,
                1029,
                1032,
                1080,
                1188,
                1258,
                1267,
                1337,
                1366,
                1372,
                1386,
                1414,
            ],
        )

    def test_comment_inside_line(self):
        filepath = Path(self.dir_path, "XMLDataObject.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [160, 165, 177, 192, 218, 279])

    def test_fake1(self):
        filepath = Path(self.dir_path, "Chain.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = StringConcatFinder()
        lines = pattern.value(ast)
        self.assertEqual(lines, [32])
