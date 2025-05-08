# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT

import unittest


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def runAnalysis(self):
        super(JavaTestCase, self).setUp()
        from aibolit.metrics.hv.main import HVMetric

        file = 'test/metrics/cc/Complicated.java'
        metric = HVMetric(file)
        res = metric.value()
        self.assertEqual(res['data'][0]['halsteadvolume'], 321.1728988800479)
        self.assertEqual(res['data'][0]['file'], file)
