# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

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
        self.assertTrue('File test/metrics/npath/ooo1.java does not exist' == str(context.exception))

    def testMediumScore(self):
        super(JavaTestCase, self).setUp()
        file = 'test/metrics/npath/Complicated.java'
        metric = NPathMetric(file)
        res = metric.value(True)
        self.assertEqual(res['data'][0]['complexity'], 12)
