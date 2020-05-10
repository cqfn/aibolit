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
import unittest
from aibolit.patterns.mutable_class.mutable_class import MutableClass


@unittest.skip('Not implemented')
class TestMutableClass(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_MutableClassFirstField(self):
        file = Path(self.dir_path, 'MutableClassFirstField.java')
        self.assertEqual(
            [1],
            MutableClass().value(file),
            'Should find mutable class having first field mutable'
        )

    def test_MutableClassMiddleField(self):
        file = Path(self.dir_path, 'MutableClassMiddleField.java')
        self.assertEqual(
            [1],
            MutableClass().value(file),
            'Should find mutable class having middle fields mutable'
        )

    def test_MutableClassLastField(self):
        file = Path(self.dir_path, 'MutableClassLastField.java')
        self.assertEqual(
            [1],
            MutableClass().value(file),
            'Should find mutable class having last field mutable'
        )

    def test_MutableClassFirstClass(self):
        file = Path(self.dir_path, 'MutableClassFirstClass.java')
        self.assertEqual(
            [1],
            MutableClass().value(file),
            'Should find mutable class in first class in file'
        )

    def test_MutableClassMiddleClass(self):
        file = Path(self.dir_path, 'MutableClassMiddleClass.java')
        self.assertEqual(
            [13],
            MutableClass().value(file),
            'Should find mutable class in class in file middle of file'
        )

    def test_MutableClassLastClass(self):
        file = Path(self.dir_path, 'MutableClassLastClass.java')
        self.assertEqual(
            [25],
            MutableClass().value(file),
            'Should find mutable class in last class in file'
        )

    def test_MutableClassMoreThanOneClass(self):
        file = Path(self.dir_path, 'MutableClassMoreThanOneClass.java')
        self.assertEqual(
            [1, 25],
            MutableClass().value(file),
            'Should find mutable class in more than one class in same file'
        )

    def test_MutableClassInnerClass(self):
        file = Path(self.dir_path, 'MutableClassInnerClass.java')
        self.assertEqual(
            [12],
            MutableClass().value(file),
            'Should find mutable fields in more than one classe in same file'
        )
