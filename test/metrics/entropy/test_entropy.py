# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from aibolit.metrics.entropy.entropy import Entropy


class EntropyTest(TestCase):
    def test_it_works(self):
        entropy_metric = Entropy()
        entropy = entropy_metric.value(
            os.path.dirname(os.path.realpath(__file__)) + '/sample-1.java'
        )
        self.assertGreaterEqual(entropy, 0)
