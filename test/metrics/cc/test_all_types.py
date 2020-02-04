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


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def runAnalysis(self):
        super(JavaTestCase, self).setUp()
        from aibolit.metrics.cc.main import CCMetric

        file = 'test/metrics/cc/Complicated.java'
        metric = CCMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 12)
        self.assertEqual(res['data'][0]['file'], file)

        with self.assertRaises(Exception) as context:
            file = 'test/metrics/cc/ooo.java'
            metric = CCMetric(file)
            res = metric.value(True)
        self.assertTrue('PMDException' in str(context.exception))

        with self.assertRaises(Exception) as context:
            file = 'test/metrics/cc/ooo1.java'
            metric = CCMetric(file)
            res = metric.value(True)
        self.assertTrue('File test/metrics/cc/ooo1.java does not exist' == str(context.exception))

        file = 'test/metrics/cc/OtherClass.java'
        metric = CCMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 3)
