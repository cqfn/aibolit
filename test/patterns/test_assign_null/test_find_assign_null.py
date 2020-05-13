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
from aibolit.patterns.assign_null_finder.assign_null_finder import NullAssignment


class TestNullAssignment(TestCase):
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    def test_several(self):
        lines = NullAssignment().value(self.cur_dir + '/several.java')
        self.assertEqual(lines, [5, 6, 11, 15, 21, 22])

    def test_one(self):
        lines = NullAssignment().value(self.cur_dir + '/one.java')
        self.assertEqual(lines, [8])

    def test_not_null(self):
        lines = NullAssignment().value(self.cur_dir + '/not_null.java')
        self.assertEqual(lines, [])
