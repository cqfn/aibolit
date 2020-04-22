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
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter
from pathlib import Path


class TestSpaces(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    max_right = IndentationCounter(max_right=True)
    max_left = IndentationCounter(max_left=True)
    left_var = IndentationCounter(left_var=True)
    right_var = IndentationCounter(right_var=True)

    def test_class_with_best_ident(self):
        val = self.max_left.value(Path(self.dir_path, 'BestIdent.java'))
        self.assertEqual(val, 44)
        val = self.max_right.value(Path(self.dir_path, 'BestIdent.java'))
        self.assertEqual(val, 113)

    def test_class_without_left_spaces(self):
        val = self.max_left.value(Path(self.dir_path, 'NoLeftSpaces.java'))
        self.assertEqual(val, 0)
        val = self.max_right.value(Path(self.dir_path, 'NoLeftSpaces.java'))
        self.assertEqual(val, 55)

    def test_class_without_right_spaces(self):
        val = self.max_left.value(Path(self.dir_path, 'NoRightSpaces.java'))
        self.assertEqual(val, 57)
        val = self.max_right.value(Path(self.dir_path, 'NoRightSpaces.java'))
        self.assertEqual(val, 0)

    def test_class_with_equal_spaces_number(self):
        val = self.max_left.value(Path(self.dir_path, 'SameMean.java'))
        self.assertEqual(val, 4)
        val = self.max_right.value(Path(self.dir_path, 'SameMean.java'))
        self.assertEqual(val, 55)

    def test_class_with_tabs_and_spaces(self):
        val = self.max_left.value(Path(self.dir_path, 'SpacesAndTabs.java'))
        self.assertEqual(val, 8)
        val = self.max_right.value(Path(self.dir_path, 'SpacesAndTabs.java'))
        self.assertEqual(val, 59)

    def test_class_with_worst_ident(self):
        val = self.max_left.value(Path(self.dir_path, 'WorstIdentation.java'))
        self.assertEqual(val, 20)
        val = self.max_right.value(Path(self.dir_path, 'WorstIdentation.java'))
        self.assertEqual(val, 163)

    def test_empty_examples(self):
        val = self.max_left.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)
        val = self.max_right.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)
        val = self.left_var.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)
        val = self.right_var.value(Path(self.dir_path, 'ClusterDataSourceConfiguration.java'))
        self.assertEqual(val, 0)

    def test_one_point_in_series(self):
        val = self.max_left.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
        val = self.max_right.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
        val = self.left_var.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
        val = self.right_var.value(Path(self.dir_path, 'package-info.java'))
        self.assertEqual(val, 0)
