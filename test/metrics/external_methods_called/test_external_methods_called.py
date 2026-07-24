# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.metrics.external_methods_called.external_methods_called import ExternalMethodsCalled
from aibolit.utils.ast_builder import build_ast


class ExternalMethodsCalledTest(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_no_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(self._ast('NoExternalMethodCalls.java')),
            0,
            'Could not calculate how many external methods are called when none'
        )

    def test_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(self._ast('ExternalMethodCalls.java')),
            2,
            'Could not calculate how many external method are called when they exist'
        )

    def test_external_method_calls_from_filepath(self):
        self.assertEqual(
            ExternalMethodsCalled().value(
                Path(self.dir_path, 'ExternalMethodCalls.java')  # ty: ignore[invalid-argument-type]
            ),
            2,
            'Could not calculate external methods from a file path'
        )

    def test_inner_class_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(self._ast('InnerClassExternalMethodCalls.java')),
            1,
            'Could not calculate how many external methods called when they exist in inner class'
        )

    def test_double_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(self._ast('DoubleExternalMethodCalls.java')),
            1,
            'Could not calculate external methods called when they are called more than once'
        )

    def test_local_method_call_is_not_external(self):
        self.assertEqual(
            ExternalMethodsCalled().value(self._ast('LocalMethodCall.java')),
            0,
            'Could not ignore local method calls'
        )

    def test_super_method_call_is_external(self):
        self.assertEqual(
            ExternalMethodsCalled().value(self._ast('SuperMethodCall.java')),
            1,
            'Could not count super method calls as external'
        )

    def _ast(self, filename):
        return AST.build_from_javalang(build_ast(Path(self.dir_path, filename)))
