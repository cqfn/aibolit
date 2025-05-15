# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
import unittest
from pathlib import Path
from unittest import TestCase

from aibolit.metrics.external_methods_called.external_methods_called import ExternalMethodsCalled


class ExternalMethodsCalledTest(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_no_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(Path(self.dir_path, 'NoExternalMethodCalls.java')),
            0,
            'Could not calculate how many external methods are called when none'
        )

    @unittest.skip('Not implemented')
    def test_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(Path(self.dir_path, 'ExternalMethodCalls.java')),
            2,
            'Could not calculate how many external method are called when they exist'
        )

    @unittest.skip('Not implemented')
    def test_inner_class_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(
                Path(self.dir_path, 'InnerClassExternalMethodCalls.java')
            ),
            1,
            'Could not calculate how many external methods called when they exist in inner class'
        )

    @unittest.skip('Not implemented')
    def test_double_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(
                Path(self.dir_path, 'DoubleExternalMethodCalls.java')
            ),
            1,
            'Could not calculate external methods called when they are called more than once'
        )
