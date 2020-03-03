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
from aibolit.metrics.npath.main import NPathMetric


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def testIncorrectFormat(self):
        super(JavaTestCase, self).setUp()
        with self.assertRaises(Exception) as context:
            file = 'test/metrics/npath/ooo.java'
            metric = NPathMetric(file)
            metric.value(True)
        self.assertTrue('PMDException' in str(context.exception))

    def testLowScore(self):
        super(JavaTestCase, self).setUp()
        file = 'test/metrics/npath/OtherClass.java'
        metric = NPathMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 3)
        self.assertEqual(res['data'][0]['file'], file)

    def testHighScore(self):
        super(JavaTestCase, self).setUp()
        file = 'test/metrics/npath/Foo.java'
        metric = NPathMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 200)
        self.assertEqual(res['data'][0]['file'], file)

    def testNonExistedFile(self):
        super(JavaTestCase, self).setUp()
        with self.assertRaises(Exception) as context:
            file = 'test/metrics/npath/ooo1.java'
            metric = NPathMetric(file)
            metric.value(True)
        self.assertTrue('File test/metrics/npath/ooo1.java does not exist' ==
                        str(context.exception))

    def testMediumScore(self):
        super(JavaTestCase, self).setUp()
        file = 'test/metrics/npath/Complicated.java'
        metric = NPathMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 12)
