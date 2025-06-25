# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import math
import os
from pathlib import Path
from unittest import TestCase, skip

import numpy as np
import pandas as pd

from aibolit.config import Config
from aibolit.model.stats import Stats
from aibolit.model.model import get_minimum, generate_fake_dataset


class TestStats(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestStats, self).__init__(*args, **kwargs)
        self.cur_file_dir = Path(os.path.realpath(__file__)).parent
        self.config = Config.get_patterns_config()

    def test_get_minimum(self):
        minimum_arr = get_minimum([0, 0.23, 0.45], [0.34, 0.01, 0.37], [0.01, 0.50, 0.2])
        self.assertTrue(np.array_equal(minimum_arr[0], np.array([0, 0.01, 0.2])))
        self.assertTrue(np.array_equal(minimum_arr[1], np.array([0, 1, 2])))

    def test_get_array(self):
        lst = [np.array([0, 1, 2, 3, 4, 5], dtype=float),
               np.array([0, 1, 2, 3, 3, 3], dtype=float)]
        x = np.array(lst)
        mask = x > 0
        ncss = np.array([0.01, 0.02])
        res = Stats.change_matrix_by_value(x, mask, 2, ncss)
        self.assertTrue(
            np.array_equal(
                res,
                np.array([[0., 1., 2.01, 3., 4., 5.],
                          [0., 1., 2.02, 3., 3., 3.]])
            )
        )

    def test_split_dataset_by_pattern_value(self):
        x = [[0, 0, 0], [0, 0, 1], [1, 1, 2]]
        nulls, not_nulls = Stats.split_dataset_by_pattern_value(x, 2)
        self.assertTrue(np.array_equal(nulls[0], np.array([0, 0, 0])))
        self.assertTrue(np.array_equal(not_nulls[0], np.array([0, 0, 1])))
        self.assertTrue(np.array_equal(not_nulls[1], np.array([1, 1, 2])))

    def __load_mock_model(self):
        config = Config.get_patterns_config()
        patterns = [x['code'] for x in config['patterns']]

        class MockModel:

            def predict(self, input: np.ndarray) -> np.ndarray:
                results = []
                for row in input:
                    s = sum(row)
                    radian = math.radians(s)
                    results.append(math.sin(radian))
                return np.array(results)

        class PatternRankingModel:

            def __init__(self):
                self.features_conf = {
                    'features_order': patterns,
                    'patterns_only': patterns
                }
                self.model = MockModel()

        return PatternRankingModel()

    @skip('Skipping test due to np.bool_ assertion issue in CI')
    def test_stat_aibolit_pipeline(self):
        model = self.__load_mock_model()
        test_df = generate_fake_dataset()
        table = Stats.aibolit_stat(test_df, model)
        test_csv = Path(self.cur_file_dir, 'results_test.csv')
        results_df = pd.read_csv(test_csv, index_col=0)
        all_elements_compared: pd.DataFrame = table.eq(results_df)
        bool_eq_elems = np.ravel(all_elements_compared.values)
        are_equal_arrays = np.logical_and.reduce(bool_eq_elems, axis=0)
        self.assertTrue(are_equal_arrays)
