# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from pathlib import Path

from aibolit.patterns.if_return_if_detection.if_detection import CountIfReturn
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class CountIfReturnTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_2nd_level_inside(self):
        filepath = Path(self.dir_path, "1.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [9, 13])

    def test_no_return_inside(self):
        filepath = Path(self.dir_path, "2.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_nested_one_goodreturn(self):
        filepath = Path(self.dir_path, "3.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_nested_one_badreturn(self):
        filepath = Path(self.dir_path, "4.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [9])

    def test_withandwithout_returns(self):
        filepath = Path(self.dir_path, "5.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [9, 17, 19, 21])

    def test_nomoreReturn_and_nested(self):
        filepath = Path(self.dir_path, "6.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = CountIfReturn()
        lines = pattern.value(ast)
        self.assertEqual(lines, [13])
