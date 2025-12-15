# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.metrics.local_methods_calls.local_methods_calls import LocalMethodsCalls
from aibolit.utils.ast_builder import build_ast


class LocalMethodsCallsTest(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def _ast_from_file(self, filename):
        filepath = Path(self.dir_path, filename)
        return AST.build_from_javalang(build_ast(filepath))

    def test_no_local_method_calls(self):
        ast = self._ast_from_file('NoLocalMethodCalls.java')
        self.assertEqual(
            LocalMethodsCalls().value(ast),
            0,
            'Could not calculate how many local methods are called when none'
        )

    def test_local_method_calls(self):
        ast = self._ast_from_file('LocalMethodCalls.java')
        self.assertEqual(
            LocalMethodsCalls().value(ast),
            4,
            'Could not calculate how many local method are called when they exist'
        )

    def test_inner_class_local_method_calls(self):
        ast = self._ast_from_file('InnerClassLocalMethodCalls.java')
        self.assertEqual(
            LocalMethodsCalls().value(ast),
            2,
            'Could not calculate how many local methods called when they exist in inner class'
        )

    def test_double_local_method_calls(self):
        ast = self._ast_from_file('DoubleLocalMethodCalls.java')
        self.assertEqual(
            LocalMethodsCalls().value(ast),
            2,
            'Could not calculate how many local methods called when they are called more than once'
        )
