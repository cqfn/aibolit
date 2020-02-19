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
from aibolit.metrics.spaces.SpaceCounter import SpacesCounter
from pathlib import Path


class TestSpaces(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent
    print(dir_path)
    pattern = SpacesCounter()

    def test_class_with_best_ident(self):
        lines = self.pattern.value(Path(self.dir_path, 'BestIdent.java'))
        assert lines[-2] == 44 and lines[-1] == 113

    def test_class_without_left_spaces(self):
        lines = self.pattern.value(Path(self.dir_path, 'NoLeftSpaces.java'))
        assert lines[-2] == 0 and lines[-1] == 55

    def test_class_without_right_spaces(self):
        lines = self.pattern.value(Path(self.dir_path, 'NoRightSpaces.java'))
        assert lines[-2] == 57 and lines[-1] == 0

    def test_class_with_equal_spaces_number(self):
        lines = self.pattern.value(Path(self.dir_path, 'SameMean.java'))
        assert lines[-2] == 4 and lines[-1] == 55

    def test_class_with_tabs_and_spaces(self):
        lines = self.pattern.value(Path(self.dir_path, 'SpacesAndTabs.java'))
        assert lines[-2] == 8 and lines[-1] == 59

    def test_class_with_worst_ident(self):
        lines = self.pattern.value(Path(self.dir_path, 'WorstIdentation.java'))
        assert lines[-2] == 20 and lines[-1] == 163
