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
from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from pathlib import Path


class TestConcatString(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    concat_finder = StringConcatFinder()

    def test_concat_strings_in_print(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'ConcatInPrint.java'))
        assert len(lines) == 1

    def test_member_plus_string(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'MemberPlusString.java'))
        assert len(lines) == 1

    def test_multiple_concat(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'MultipleConcat.java'))
        assert len(lines) == 1

    def test_empty_case(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'Nothing.java'))
        assert len(lines) == 0

    def test_string_plus_member(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'StringPlusMember.java'))
        assert len(lines) == 1

    def test_many_concats(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'ManyConcats.java'))
        assert len(lines) == 4

    def test_concat_in_different_methods(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'DifferentMethods.java'))
        assert len(lines) == 2

    def test_fake_operator_plus(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'FakePlusOperator.java'))
        assert len(lines) == 0
