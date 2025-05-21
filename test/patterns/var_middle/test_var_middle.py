# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.var_middle.var_middle import VarMiddle
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class VarMiddleTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_good_class(self):
        filepath = self.current_directory / "1.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_bad_class(self):
        filepath = self.current_directory / "2.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [12, 19])

    def test_case_with_multiline_method_declaration(self):
        filepath = self.current_directory / "3.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_case_with_empty_lines(self):
        filepath = self.current_directory / "4.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_case_autoclosable(self):
        filepath = self.current_directory / "5.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_case_nested_class(self):
        filepath = self.current_directory / "6.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [33, 36])

    def test_declaration_after_super_class_method_call(self):
        filepath = self.current_directory / "7.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [17])

    def test_for_scope_good(self):
        filepath = self.current_directory / "8.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_for_scope_bad(self):
        filepath = self.current_directory / "9.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [14])

    def test_variable_declared_after_for(self):
        filepath = self.current_directory / "10.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [14])

    def test_11(self):
        filepath = self.current_directory / "11.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_catch_good(self):
        filepath = self.current_directory / "12.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_catch_bad(self):
        filepath = self.current_directory / "13.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [41])

    def test_else_bad(self):
        filepath = self.current_directory / "14.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [90])

    def test_variable_after_curly_braces(self):
        filepath = self.current_directory / "15.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_variable_inside_lambda(self):
        filepath = self.current_directory / "16.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_annotation_with_parameters(self):
        filepath = self.current_directory / "17.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = VarMiddle()
        lines = pattern.value(ast)
        self.assertEqual(lines, [25])
