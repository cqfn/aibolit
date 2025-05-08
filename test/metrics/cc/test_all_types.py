# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

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
