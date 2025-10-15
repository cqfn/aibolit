# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import dataclasses
from decimal import localcontext, ROUND_DOWN, Decimal
from typing import Dict, Any, Tuple, List
from numpy.typing import NDArray

import numpy as np
import pandas as pd
from catboost import CatBoost
from sklearn.base import BaseEstimator

from aibolit.config import Config


def get_minimum(
        c1: NDArray[np.float64],
        c2: NDArray[np.float64],
        c3: NDArray[np.float64]) -> Tuple[NDArray[np.float64], NDArray[np.int64]]:
    """
    Args:
        c1, c2, c3: np.array with shape (number of snippets, ).
    Returns:
        c: np.array with shape (number of snippets, ) -
        elemental minimum of 3 arrays.
        number: np.array with shape (number of snippets, ) of
        arrays' numbers with minimum elements.            .
    """

    c: NDArray[np.float64] = np.vstack((c1, c2, c3))

    return np.min(c, 0), np.argmin(c, 0)


def generate_fake_dataset() -> pd.DataFrame:
    config = Config.get_patterns_config()
    patterns = [x['code'] for x in config['patterns']]
    metrics = [x['code'] for x in config['metrics']]

    train_df = pd.DataFrame(columns=patterns)
    min_rows_for_train = 10
    for x in range(min_rows_for_train):
        p = {p: (x + i) for i, p in enumerate(patterns)}
        m = {p: (x + i) for i, p in enumerate(metrics)}
        row = {**p, **m}
        train_df = pd.concat([train_df, pd.DataFrame([row])], ignore_index=True)

    train_df = train_df.astype(float)
    return train_df


def scale_dataset(
        df: pd.DataFrame,
        features_conf: Dict[Any, Any],
        target_metric_code: str,
        scale_ncss: bool = True) -> pd.DataFrame:
    config = Config.get_patterns_config()
    patterns_codes_set = set([x['code'] for x in config['patterns']])
    metrics_codes_set = set([x['code'] for x in config['metrics']])
    exclude_features = (set(config['patterns_exclude']).union(
        set(config['metrics_exclude'])))
    used_codes = set(features_conf['features_order'])
    used_codes.add(target_metric_code)
    not_scaled_codes = (set(patterns_codes_set).union(set(metrics_codes_set))
                        .difference(used_codes).difference(exclude_features))
    features_not_in_config: List[str] = list(
        set(df.columns).difference(not_scaled_codes).difference(used_codes))
    not_scaled_codes_list: List[str] = sorted(
        list(not_scaled_codes.union(set(features_not_in_config))))
    codes_to_scale = sorted(used_codes)
    if scale_ncss:
        scaled_df = pd.DataFrame(
            df[codes_to_scale].values / np.array(df['M2'].values).reshape((-1, 1)),
            columns=codes_to_scale
        )
        not_scaled_df = df[not_scaled_codes_list]
        input = pd.concat([scaled_df, not_scaled_df], axis=1)
    else:
        input = df

    return input


@dataclasses.dataclass()
class PatternRankingModel(BaseEstimator):
    do_rename_columns: bool = False
    model: CatBoost | None = None
    features_conf: Dict[Any, Any] = dataclasses.field(default_factory=dict)

    def predict(self, input_params: Dict[Any, Any]) -> Tuple[Dict[Any, int], List[float]]:
        features_order = self.features_conf['features_order']
        # add ncss to last column. We will normalize all patterns by that value
        input = np.array([input_params[i] for i in features_order] + [input_params['M2']])
        preds, importances = self.rank(input)

        return ({features_order[int(x)]: int(x) for x in preds},
                list(importances))

    def fit_regressor(
            self,
            X: NDArray,
            y: NDArray,
            features: Any = None,
            display: bool = False) -> None:
        """

        :param X: X np.array with shape (number of snippets, number of patterns) or
                (number of patterns, ).
        :param y: np.array with shape (number of snippets,), array of snippets'
                complexity metric values
        :param features: set of features to train
        :param display: show additional output
        :return: None
        """
        model = CatBoost()

        grid = {'learning_rate': [0.03, 0.1],
                'depth': [4, 6, 10],
                'l2_leaf_reg': [1, 3, 5, 7, 9]}
        if features:
            X = X[features]

        if hasattr(X, 'columns'):
            self.features_conf = {'features_order': list(X.columns)}
        else:
            self.features_conf = {'features_order': list(range(X.shape[1]))}

        model.grid_search(
            grid,
            X=X,
            y=y,
            verbose=display,
        )

        self.model = model
        self.model.fit(X, y, logging_level='Silent')

    def sigmoid(self, x: float) -> float:
        return float(1 / (1 + np.exp(-x)))

    def __get_pairs(
            self,
            item: NDArray,
            th: float,
            feature_importances: Any = None) -> Tuple[NDArray, NDArray]:
        assert isinstance(self.model, CatBoost)
        if not feature_importances:
            feature_importances = self.model.feature_importances_
        pattern_importances = item * feature_importances
        # mask discards not significant patterns
        th_mask = (self.sigmoid(pattern_importances) <= th) + 0
        pattern_importances = pattern_importances * th_mask
        order = np.arange(self.model.feature_importances_.size)
        return (pattern_importances, order)

    def __vstack_arrays(self, res: List[NDArray]) -> NDArray:
        return np.vstack(res).T

    def calculate_score(
            self,
            X: NDArray,
            quantity_func: str = 'log',
            th: float = 1.0,
            feature_importances: Any = None) -> Tuple[NDArray, List[float]]:
        """
        Args:
            X: np.array with shape ( number of patterns).
            quantity_func: str, type of function that will be applied to
                number of occurrences.
            th (float): Sensitivity of algorithm to recommend.
                0 - ignore all recommendations
                1 - use all recommendations

        Returns:
            ranked: np.array with shape (number of snippets, number of patterns)
                of sorted patterns in non-increasing order for each snippet of
                code.
        """

        X = X.copy()
        X = np.expand_dims(X, axis=0)

        ranked = []
        quantity_funcs = {
            'log': lambda x: np.log1p(x) / np.log(10),
            'exp': lambda x: np.exp(x + 1),
            'linear': lambda x: x,
        }

        try:
            item = quantity_funcs[quantity_func](X)
            pattern_importances, order = self.__get_pairs(item, th, feature_importances)
            pairs = self.__vstack_arrays([pattern_importances, order])
            pairs = pairs[pairs[:, 0].argsort()]
            ranked.append(pairs[:, 1].T.tolist()[::-1])
        except Exception:
            import traceback
            traceback.print_exc()
            raise Exception('Unknown func')

        return (np.array(ranked), pairs[:, 0].T.tolist()[::-1])

    def rank(self, snippet: NDArray, scale: bool = True) -> Tuple[List[int], List[float]]:
        """
        Args:
            snippet: np.array with shape (number of snippets, number of patterns + 1),
            because last column is ncss
        Returns:
            ranked: np.array with shape (number of snippets, number of patterns)
                of sorted patterns in non-increasing order for each snippet of
                code.
        """

        # remember it, since we will use `log` function for non-normalized input value
        patterns_orig = np.array(snippet[:-1])
        ncss = snippet[-1]

        if scale:
            snippet = patterns_orig / ncss
        else:
            snippet = patterns_orig

        k = snippet.size
        assert isinstance(self.model, CatBoost)
        complexity = float(self.model.predict(snippet))
        importances = []
        for i in range(k):
            if snippet[i] == 0:
                # do not need to predict if we have 0
                importances.append((i, 0))
                continue
            temp_arr = snippet.copy()
            temp_arr[i] = temp_arr[i] - (1 / ncss)
            complexity_minus = float(self.model.predict(temp_arr))
            if complexity_minus < complexity:
                # complexity decreased
                with localcontext() as ctx:
                    ctx.rounding = ROUND_DOWN
                    abs_diff = abs(complexity - complexity_minus)
                    diff_decimal = Decimal(abs_diff).quantize(Decimal('0.001'))
                    diff = float(diff_decimal * 100)
            else:
                # complexity increased, we do not need such value, set to 0,
                # cause we need only patterns when complexity decreased
                diff = 0.0
            importances.append((i, int(diff)))

        sorted_importances = dict(sorted(importances, key=lambda x: x[1], reverse=True))
        return (
            list(sorted_importances.keys()),
            list(sorted_importances.values())
        )
