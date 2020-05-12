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
import unittest
from aibolit.metrics.external_methods_called.external_methods_called import ExternalMethodsCalled
from pathlib import Path
from unittest import TestCase


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
            ExternalMethodsCalled().value(Path(self.dir_path, 'InnerClassExternalMethodCalls.java')),
            1,
            'Could not calculate how many external methods called when they exist in inner class'
        )

    @unittest.skip('Not implemented')
    def test_double_external_method_calls(self):
        self.assertEqual(
            ExternalMethodsCalled().value(Path(self.dir_path, 'DoubleExternalMethodCalls.java')),
            1,
            'Could not calculate how many external methods called when they are called more than once'
        )
