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
from aibolit.metrics.cognitiveC.cognitive_c import CognitiveComplexity
from pathlib import Path


class TestCognitive(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    get_cc = CognitiveComplexity()

    def test1(self):
        lines = self.get_cc.value(Path(self.dir_path, '1.java'))
        self.assertEqual(lines, 7)

    def test2(self):
        lines = self.get_cc.value(Path(self.dir_path, '2.java'))
        self.assertEqual(lines, 9)

    def test3(self):
        lines = self.get_cc.value(Path(self.dir_path, '3.java'))
        self.assertEqual(lines, 10)

    def test4(self):
        lines = self.get_cc.value(Path(self.dir_path, '4.java'))
        self.assertEqual(lines, 6)

    def test5(self):
        lines = self.get_cc.value(Path(self.dir_path, '5.java'))
        self.assertEqual(lines, 3)

    def test6(self):
        lines = self.get_cc.value(Path(self.dir_path, '6.java'))
        self.assertEqual(lines, 14)

    def test7(self):
        lines = self.get_cc.value(Path(self.dir_path, 'recursion.java'))
        self.assertEqual(lines, 6)

    def test8(self):
        lines = self.get_cc.value(Path(self.dir_path, 'nested.java'))
        self.assertEqual(lines, 9)

    def test9(self):
        lines = self.get_cc.value(Path(self.dir_path, '7.java'))
        self.assertEqual(lines, 17)

    def test10(self):
        lines = self.get_cc.value(Path(self.dir_path, '8.java'))
        self.assertEqual(lines, 13)
