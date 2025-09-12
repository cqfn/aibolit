# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.metrics.external_methods_called.external_methods_called import ExternalMethodsCalled
from aibolit.utils.ast_builder import build_ast


class ExternalMethodsCalledTest(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def _ast_from_file(self, filename):
        filepath = Path(self.dir_path, filename)
        return AST.build_from_javalang(build_ast(filepath))

    def test_no_external_method_calls(self):
        ast = self._ast_from_file('NoExternalMethodCalls.java')
        self.assertEqual(
            ExternalMethodsCalled().value(ast),
            0,
            'Could not calculate how many external methods are called when none'
        )

    def test_external_method_calls(self):
        ast = self._ast_from_file('ExternalMethodCalls.java')
        self.assertEqual(
            ExternalMethodsCalled().value(ast),
            2,
            'Could not calculate how many external method are called when they exist'
        )

    def test_inner_class_external_method_calls(self):
        ast = self._ast_from_file('InnerClassExternalMethodCalls.java')
        self.assertEqual(
            ExternalMethodsCalled().value(ast),
            1,
            'Could not calculate how many external methods called when they exist in inner class'
        )

    def test_double_external_method_calls(self):
        ast = self._ast_from_file('DoubleExternalMethodCalls.java')
        self.assertEqual(
            ExternalMethodsCalled().value(ast),
            1,
            'Could not calculate external methods called when they are called more than once'
        )
