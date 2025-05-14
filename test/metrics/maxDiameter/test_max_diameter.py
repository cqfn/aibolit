# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.metrics.max_diameter.max_diameter import MaxDiameter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class MaxDiameterTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test1(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '1.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 20)

    def test2(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '2.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 14)

    def test3(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '3.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 7)

    def test4(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '4.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 10)

    def test5(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '5.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 11)

    def test6(self):
        ast = AST.build_from_javalang(build_ast(self.current_directory / '6.java'))
        metric = MaxDiameter()
        metric_value = metric.value(ast)
        self.assertEqual(metric_value, 8)
