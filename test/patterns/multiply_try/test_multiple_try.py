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
from aibolit.patterns.multiple_try.multiple_try import MultipleTry
from pathlib import Path


class TestMultipleTry(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    method_chain_finder = MultipleTry()

    def test_simple(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'Simple.java'))
        self.assertEqual(lines, [2])

    def test_large_file(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'Large.java'))
        self.assertEqual(lines, [620, 706])

    def test_try_inside_anonymous(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'TryInsideAnomymous.java'))
        self.assertEqual(lines, [5])

    def test_try_inside_catch(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'TryInsideCatch.java'))
        self.assertEqual(lines, [2])

    def test_try_inside_finally(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'TryInsideFinaly.java'))
        self.assertEqual(lines, [2])

    def test_try_inside_try(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'TryInsideTry.java'))
        self.assertEqual(lines, [2])

    def test_try_method_overloading(self):
        lines = self.method_chain_finder.value(Path(self.dir_path, 'TryMethodOverloading.java'))
        self.assertEqual(lines, [])
