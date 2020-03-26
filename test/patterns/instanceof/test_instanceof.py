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
from aibolit.patterns.instanceof.instance_of import InstanceOf
from pathlib import Path


class TestInstanceOf(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    testClass = InstanceOf()

    def test_empty(self):
        file = str(Path(self.cur_file_dir, 'Empty.java'))
        self.assertEqual(len(self.testClass.value(file)), 0)

    def test_instance_of(self):
        file = str(Path(self.cur_file_dir, 'InstanceOfSample.java'))
        self.assertEqual(len(self.testClass.value(file)), 1)

    def test_instance(self):
        file = str(Path(self.cur_file_dir, 'InstanceSample.java'))
        self.assertEqual(len(self.testClass.value(file)), 1)

    def test_instance_of_different_methods(self):
        file = str(Path(self.cur_file_dir, 'InstanceOfSampleDifferentMethods.java'))
        self.assertEqual(len(self.testClass.value(file)), 2)

    def test_instance_different_methods(self):
        file = str(Path(self.cur_file_dir, 'InstanceSampleDifferentMethods.java'))
        self.assertEqual(len(self.testClass.value(file)), 2)

    def test_instance_of_several(self):
        file = str(Path(self.cur_file_dir, 'InstanceOfSampleSeveral.java'))
        self.assertEqual(len(self.testClass.value(file)), 3)

    def test_instance_several(self):
        file = str(Path(self.cur_file_dir, 'InstanceSampleSeveral.java'))
        self.assertEqual(len(self.testClass.value(file)), 2)

    def test_instance_in_method_chaining(self):
        file = str(Path(self.cur_file_dir, 'InstanceSampleChain.java'))
        self.assertEqual(len(self.testClass.value(file)), 2)

    def test_both(self):
        file = str(Path(self.cur_file_dir, 'InstanceBoth.java'))
        self.assertEqual(len(self.testClass.value(file)), 2)
