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
        file = 'test/metrics/ncss/GraalSDK.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 2)

    def testMediumScore(self):
        file = 'test/metrics/ncss/WorkflowRunActionRepetitionDefinitionInner.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 73)

    def testHighScore(self):
        file = 'test/metrics/ncss/YarnConfiguration.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 1301)

    def testBasicExample(self):
        file = 'test/metrics/ncss/BasicExample.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 12)

    def testAnotherScore(self):
        file = 'test/metrics/ncss/WebAppsImpl.java'
        metric = NCSSMetric()
        res = metric.value(file)
        self.assertEqual(res, 1429)
