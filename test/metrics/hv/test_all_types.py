# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import unittest

from aibolit.metrics.hv.main import HVMetric


class JavaTestCase(unittest.TestCase):
    def runAnalysis(self):
        file = 'test/metrics/cc/Complicated.java'
        metric = HVMetric(file)
        res = metric.value()
        self.assertEqual(res['data'][0]['halsteadvolume'], 321.1728988800479)
        self.assertEqual(res['data'][0]['file'], file)
