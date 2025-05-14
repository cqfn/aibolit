# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.metrics.NumberMethods.NumberMethods import NumberMethods
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class TestCognitive(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_one(self):
        filepath = self.current_directory / 'one.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = NumberMethods()
        value = metric.value(ast)
        self.assertEqual(value, 1)

    def test_simple(self):
        filepath = self.current_directory / 'simple.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = NumberMethods()
        value = metric.value(ast)
        self.assertEqual(value, 2)

    def test_nested(self):
        filepath = self.current_directory / 'nested.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = NumberMethods()
        value = metric.value(ast)
        self.assertEqual(value, 2)

    def test_several(self):
        filepath = self.current_directory / 'several.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        metric = NumberMethods()
        value = metric.value(ast)
        self.assertEqual(value, 4)
