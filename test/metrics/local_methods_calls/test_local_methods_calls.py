# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
import unittest
from pathlib import Path
from unittest import TestCase

from aibolit.metrics.local_methods_calls.local_methods_calls import LocalMethodsCalls


class LocalMethodsCallsTest(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_no_local_method_calls(self):
        self.assertEqual(
            LocalMethodsCalls().value(Path(self.dir_path, 'NoLocalMethodCalls.java')),
            0,
            'Could not calculate how many local methods are called when none'
        )

    @unittest.skip('Not implemented')
    def test_local_method_calls(self):
        self.assertEqual(
            LocalMethodsCalls().value(Path(self.dir_path, 'LocalMethodCalls.java')),
            4,
            'Could not calculate how many local method are called when they exist'
        )

    @unittest.skip('Not implemented')
    def test_inner_class_local_method_calls(self):
        self.assertEqual(
            LocalMethodsCalls().value(Path(self.dir_path, 'InnerClassLocalMethodCalls.java')),
            2,
            'Could not calculate how many local methods called when they exist in inner class'
        )

    @unittest.skip('Not implemented')
    def test_double_local_method_calls(self):
        self.assertEqual(
            LocalMethodsCalls().value(Path(self.dir_path, 'DoubleLocalMethodCalls.java')),
            2,
            'Could not calculate how many local methods called when they are called more than once'
        )
