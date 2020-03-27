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
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from pathlib import Path


class TestNestedBlocks(TestCase):
    depth_level = 2
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    testClass = NestedBlocks(depth_level)

    def test_single_for_loop(self):
        file = str(Path(self.cur_file_dir, 'SingleFor.java'))
        self.assertEqual(self.testClass.value(file), [15, 19])

    def test_nested_for_loops(self):
        file = str(Path(self.cur_file_dir, 'NestedFor.java'))
        self.assertEqual(self.testClass.value(file), [22])

    def test_for_loops_in_different_methods(self):
        file = str(Path(self.cur_file_dir, 'DifferentMethods.java'))
        self.assertEqual(self.testClass.value(file), [28])

    def test_for_loops_in_nested_class(self):
        file = str(Path(self.cur_file_dir, 'NestedForInNestedClasses.java'))
        self.assertEqual(self.testClass.value(file), [9])

    def test_for_loops_in_anonymous_class(self):
        file = str(Path(self.cur_file_dir, 'ForInAnonymousFile.java'))
        self.assertEqual(self.testClass.value(file), [19])

    def test_nested_no_nested_if(self):
        pattern = NestedBlocks(2, BlockType.IF)
        file = str(Path(self.cur_file_dir, 'NestedNoIF.java'))
        self.assertEqual(pattern.value(file), [])

    def test_nested_if(self):
        pattern = NestedBlocks(2, BlockType.IF)
        file = str(Path(self.cur_file_dir, 'NestedIF.java'))
        self.assertEqual(pattern.value(file), [21, 42])
