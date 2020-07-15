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
from aibolit.patterns.supermethod.supermethod import SuperMethod
from pathlib import Path


class TestSuperMethod(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    testClass = SuperMethod()

    def test_empty(self):
        file = str(Path(self.cur_file_dir, 'Empty.java'))
        self.assertEqual(len(self.testClass.value(file)), 0)

    def test_instance_of(self):
        # It has 2 matches in anonymous class!
        file = str(Path(self.cur_file_dir, 'Anonymous.java'))
        self.assertEqual(len(self.testClass.value(file)), 1)

    def test_instance(self):
        file = str(Path(self.cur_file_dir, 'Simple.java'))
        self.assertEqual(len(self.testClass.value(file)), 1)

    def test_several(self):
        # It has 2 matches in anonymous class!
        file = str(Path(self.cur_file_dir, 'Several.java'))
        self.assertEqual(len(self.testClass.value(file)), 6)

    def test_nested_class(self):
        file = str(Path(self.cur_file_dir, 'NestedClass.java'))
        self.assertEqual(len(self.testClass.value(file)), 1)

    def test_constructor(self):
        file = str(Path(self.cur_file_dir, 'Constructor.java'))
        self.assertEqual(len(self.testClass.value(file)), 3)

    def test_complicated_constructor(self):
        file = str(Path(self.cur_file_dir, 'ComplicatedChainConstructor.java'))
        self.assertEqual(len(self.testClass.value(file)), 0)
