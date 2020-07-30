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

import unittest
from aibolit.metrics.ncss.ncss import NCSSMetric


class TestNCSSMetric(unittest.TestCase):
    def testZeroScore(self):
        file = 'test/metrics/ncss/Empty.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 0)

    def testLowScore(self):
        file = 'test/metrics/ncss/Simple.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 2)

    def testBasicExample(self):
        file = 'test/metrics/ncss/BasicExample.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 13)

    def testSimpleExample(self):
        file = 'test/metrics/ncss/SimpleExample.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 18)

    def testSimpleExample2(self):
        file = 'test/metrics/ncss/SimpleExample2.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 19)

    def testChainedIfElse(self):
        file = 'test/metrics/ncss/ChainedIfElse.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 11)

    def testChainedIfElseWithTrailingElse(self):
        file = 'test/metrics/ncss/ChainedIfElseWithTrailingElse.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 12)

    def testFinallyBlock(self):
        file = 'test/metrics/ncss/FinallyBlock.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 7)
