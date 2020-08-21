# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
        self.assertEqual(lines, [12])

    def test_controller_in_end(self):
        filepath = Path(self.dir_path, "AnimatableTransform.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [12])

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
        self.assertEqual(lines, [18, 186])

    def test_class_parser(self):
        filepath = Path(self.dir_path, "Configuration.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ErClass()
        lines = pattern.value(ast)
        self.assertEqual(lines, [3106])

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
        self.assertEqual(lines, [837, 1478, 1538, 1684])
