# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from pathlib import Path

from aibolit.patterns.er_class.er_class import ErClass
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class ErClassTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_manager_in_middle(self):
        filepath = Path(self.dir_path, "AnimatableSplitDimensionPathValue.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])

    def test_controller_in_end(self):
        filepath = Path(self.dir_path, "AnimatableTransform.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])

    def test_one_normal_class(self):
        filepath = Path(self.dir_path, "AuditEventModelProcessor.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_two_classes_with_pattern(self):
        filepath = Path(self.dir_path, "BaseKeyframeAnimation.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [21, 189])

    def test_class_parser(self):
        filepath = Path(self.dir_path, "Configuration.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [3109])

    def test_another_normal_class(self):
        filepath = Path(self.dir_path, "FillContent.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_four_normal_classes(self):
        filepath = Path(self.dir_path, "FJIterateTest.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_two_distant_normal_classes(self):
        filepath = Path(self.dir_path, "FJListProcedureRunner.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_classes_in_comments(self):
        filepath = Path(self.dir_path, "KeyProviderCryptoExtension.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_classes_in_methods(self):
        filepath = Path(self.dir_path, "OsSecureRandom.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_normal_class(self):
        filepath = Path(self.dir_path, "RectangleContent.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_three_writers_one_reader(self):
        filepath = Path(self.dir_path, "SequenceFile.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [840, 1481, 1541, 1687])
