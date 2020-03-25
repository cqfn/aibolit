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
        self.assertEqual(lines,  [14])

    def test_member_plus_string(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'MemberPlusString.java'))
        self.assertEqual(lines,  [111])

    def test_multiple_concat(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'MultipleConcat.java'))
        self.assertEqual(lines,  [22])

    def test_empty_case(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'Nothing.java'))
        self.assertEqual(lines,  [])

    def test_string_plus_member(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'StringPlusMember.java'))
        self.assertEqual(len(lines), 1)

    def test_many_concats(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'ManyConcats.java'))
        self.assertEqual(lines,  [22, 23, 24, 25])

    def test_concat_in_different_methods(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'DifferentMethods.java'))
        self.assertEqual(lines,  [13, 27])

    def test_fake_operator_plus(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'FakePlusOperator.java'))
        self.assertEqual(lines,  [])

    def test_giant_file(self):
        lines = self.concat_finder.value(Path(self.dir_path, 'CliFlags.java'))
        self.assertEqual(lines,  [
            34, 35, 36, 37, 51, 53, 297, 298, 82, 83, 84, 85, 86, 87, 88, 197,
            90, 91, 92, 297, 211, 298, 96, 97, 98, 112, 113, 127, 128, 129, 130,
            131, 132, 146, 148, 149, 150, 151, 153, 155, 156, 157, 158, 159, 173,
            174, 188, 189, 190, 191, 192, 193, 194, 197, 198, 199, 200, 204, 207,
            208, 209, 211, 212, 214, 215, 216, 230, 231, 232, 233, 236, 239, 240,
            241, 242, 243, 244, 245, 259, 260, 261, 262, 263, 264, 278, 279, 280,
            299, 282, 283, 297, 298, 299, 300, 314, 315, 316, 317, 318, 319, 320,
            321, 325, 326, 329, 331, 332, 333, 335, 336, 339, 340, 341, 343, 345,
            347, 348, 349
        ])
