# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.send_null.send_null import SendNull
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class SendNullTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_one_send(self):
        filepath = self.current_directory / "BaseKeyframeAnimation.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [149])

    def test_multi_level_invocation(self):
        filepath = self.current_directory / "Configuration.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(
            lines,
            [382, 445, 552, 641, 659, 833, 869, 1365, 2396, 2877, 2991, 3083, 3495, 3761, 3858]
        )

    def test_no_null_methods(self):
        filepath = self.current_directory / "FillContent.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple_invocation(self):
        filepath = self.current_directory / "FJIterateTest.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [489])

    def test_more_method_invocations(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [1100, 1189, 1204, 1220, 3288, 3301, 3370, 3540, 3553])

    def test_constructor_send_null(self):
        filepath = self.current_directory / "Constructor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [8, 17, 18, 19, 20, 21])

    def test_super_in_constructor_with_ternary_operator(self):
        filepath = self.current_directory / "AclPermissionParam.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [49, 53])

    def test_this_with_ternary_operator(self):
        filepath = self.current_directory / "AddOp.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [31, 35])

    def test_super_in_constructor_with_method_inv(self):
        filepath = self.current_directory / "ByteArrayMultipartFileEditor.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [51])
