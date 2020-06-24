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

import numpy as np
from unittest import TestCase
from aibolit.model.model import TwoFoldRankingModel


class TestModel(TestCase):

    def test_get_minimum(self):
        ranking_model = TwoFoldRankingModel()
        c1 = np.array([1, 4, 5, 3, 6, 6, 4, 3, 1])
        c2 = np.array([1, 2, 7, 3, 8, 4, 5, 3, -1])
        c3 = np.array([1, 4, 5, 7, 6, 3, 0, -3, 1])
        c, number = ranking_model.get_minimum(c1, c2, c3)
        np.testing.assert_array_equal(c, np.array([1, 2, 5, 3, 6, 3, 0, -3, -1]))
        np.testing.assert_array_equal(number, np.array([0, 1, 0, 0, 0, 2, 2, 2, 1]))
