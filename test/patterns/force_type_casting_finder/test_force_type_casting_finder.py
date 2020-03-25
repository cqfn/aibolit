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
from aibolit.patterns.force_type_casting_finder import force_type_casting_finder


class ForceTypeCastingFinderTest(TestCase):
    def test_simple(self):
        pattern = force_type_casting_finder.ForceTypeCastingFinder()
        lines = pattern.value(
            os.path.dirname(os.path.realpath(__file__)) + '/1.java')
        self.assertEqual(lines, [5])

    def test_several_casts(self):
        pattern = force_type_casting_finder.ForceTypeCastingFinder()
        lines = pattern.value(
            os.path.dirname(os.path.realpath(__file__)) + '/2.java')
        self.assertEqual(lines, [5, 11, 17])

    def test_zero_lines(self):
        pattern = force_type_casting_finder.ForceTypeCastingFinder()
        lines = pattern.value(
            os.path.dirname(os.path.realpath(__file__)) + '/3.java')
        self.assertEqual(lines, [])
