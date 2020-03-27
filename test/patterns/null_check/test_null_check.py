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
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.null_check.null_check import NullCheck


class TestNullCheck(TestCase):
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    testClass = NullCheck()

    def test_null_check(self):
        file = Path(self.cur_file_dir, 'NullCheck.java')

        self.assertEqual(self.testClass.value(file), [5])

    def test_null_check_in_constructor(self):
        file = Path(self.cur_file_dir, 'NullCheckInConstructor.java')

        self.assertEqual(self.testClass.value(file), [])
