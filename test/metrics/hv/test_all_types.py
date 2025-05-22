# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import unittest

from aibolit.metrics.hv.main import HVMetric


class JavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(JavaTestCase, cls).setUpClass()

    def runAnalysis(self):
        super(JavaTestCase, self).setUp()
        file = 'test/metrics/cc/Complicated.java'
        metric = HVMetric(file)
        res = metric.value()
        self.assertEqual(res['data'][0]['halsteadvolume'], 321.1728988800479)
        self.assertEqual(res['data'][0]['file'], file)
