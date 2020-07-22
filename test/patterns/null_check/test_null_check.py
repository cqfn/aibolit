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
from aibolit.patterns.null_check.null_check import NullCheck
from pathlib import Path


class TestNullCheck(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    class_to_test = NullCheck()

    def test_null_check(self):
        lines = self.class_to_test.value(Path(self.dir_path, '1.java'))
        self.assertEqual(lines, [4])

    def test_null_check_in_constructor(self):
        lines = self.class_to_test.value(Path(self.dir_path, '2.java'))
        self.assertEqual(lines, [])

    def test_null_check_comparison_result_assignment(self):
        lines = self.class_to_test.value(Path(self.dir_path, '3.java'))
        self.assertEqual(lines, [4])

    def test_null_check_ternary(self):
        lines = self.class_to_test.value(Path(self.dir_path, '4.java'))
        self.assertEqual(lines, [4])

    def test_null_check_not_equal_comparison(self):
        lines = self.class_to_test.value(Path(self.dir_path, '5.java'))
        self.assertEqual(lines, [4])
