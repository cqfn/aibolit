# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.metrics.cognitiveC.cognitive_c import CognitiveComplexity
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class CognitiveComplexityTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test1(self):
        filepath = self.current_directory / '1.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 7)

    def test2(self):
        filepath = self.current_directory / '2.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 9)

    def test3(self):
        filepath = self.current_directory / '3.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 10)

    def test4(self):
        filepath = self.current_directory / '4.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 6)

    def test5(self):
        filepath = self.current_directory / '5.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 3)

    def test6(self):
        filepath = self.current_directory / '6.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 14)

    def test7(self):
        filepath = self.current_directory / 'recursion.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 6)

    def test8(self):
        filepath = self.current_directory / 'nested.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 9)

    def test9(self):
        filepath = self.current_directory / '7.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 17)

    def test10(self):
        filepath = self.current_directory / '8.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = CognitiveComplexity()
        value = metric.value(ast)
        self.assertEqual(value, 13)
