from typing import List

import numpy as np
import pandas as pd
from catboost import CatBoost
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler

from aibolit.config import Config


class Dataset:

    def __init__(self, only_patterns: List[str]):
        self.input = None
        self.target = None
        self.do_rename_columns = False
        self.only_patterns = only_patterns

    def preprocess_file(
            self,
            scale_ncss=True,
            scale=False,
            **kwargs):

        print('reading dataset from {}'.format(Config.dataset_file()))
        df = pd.read_csv(Config.dataset_file())
        df = df[~df["filename"].str.lower().str.contains("test")]
        config = Config.get_patterns_config()
        if self.do_rename_columns:
            p_codes = \
                [x['code'] for x in config['patterns']] \
                + ['lines' + x['code'] for x in config['patterns']]
            m_codes = [x['code'] for x in config['metrics']]
            keys = p_codes + m_codes
            vals = \
                [x['name'] for x in config['patterns']] \
                + ['lines' + x['name'] for x in config['patterns']] \
                + [x['name'] for x in config['metrics']]

            replace_dict = dict(zip(keys, vals))
            df = df.rename(replace_dict)
            df.columns = vals
            print('Columns renamed:' + df.head())

        df = df.dropna().drop_duplicates(subset=df.columns.difference(['filename']))
        df = df[(df.ncss > 20) & (df.ncss < 100) & (df.npath_method_avg < 100000.00)].copy().reset_index()

        df.drop('filename', axis=1, inplace=True)
        df.drop('index', axis=1, inplace=True)
        self.target = np.array(df[['M4']].values[:, 0], dtype=np.float64)
        if scale_ncss:
            new = pd.DataFrame(
                df[self.only_patterns].values / df['M2'].values.reshape((-1, 1)),
                columns=self.only_patterns
            )
            self.target /= df['M2'].values.reshape(-1)
        else:
            new = df[self.only_patterns].copy()
        if scale:
            self.input = pd.DataFrame(StandardScaler().fit_transform(new.values), columns=new.columns,
                                      index=new.index).values
        else:
            self.input = new.values

        self.feature_order = list(new.columns)


class TwoFoldRankingModel(BaseEstimator):

    def __init__(self):
        self.do_rename_columns = False
        self.model = None
        self.features_conf = None

    def fit(self, X, y, display=False):
        """
        Args:
            X: np.array with shape (number of snippets, number of patterns) or
                (number of patterns, ).
            y: np.array with shape (number of snippets,), array of snippets'
                complexity metric values
            display: bool, to output info about training or not
        """
        model = CatBoost()

        grid = {'learning_rate': [0.03, 0.1],
                'depth': [4, 6, 10],
                'l2_leaf_reg': [1, 3, 5, 7, 9]}

        model.grid_search(
            grid,
            X=X,
            y=y,
            verbose=display,
        )

        self.model = model
        self.model.fit(X, y.ravel(), logging_level='Silent')

    def __get_pairs(self, item, th: float):
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        pattern_importances = item * self.model.feature_importances_
        # mask discards not significant patterns
        th_mask = (sigmoid(pattern_importances) <= th) + 0
        pattern_importances = pattern_importances * th_mask
        order = np.arange(self.model.feature_importances_.size)
        return (pattern_importances, order)

    def __vstack_arrays(self, res):
        return np.vstack(res).T

    def predict(self, X, quantity_func='log', th=1.0):
        """
        Args:
            X: np.array with shape (number of snippets, number of patterns) or
                (number of patterns, ).
            quantity_func: str, type of function that will be applied to
                number of occurrences.
            th (float): Sensitivity of algorithm to recommend.
                0 - ignore all recomendations
                1 - use all recommendations

        Returns:
            ranked: np.array with shape (number of snippets, number of patterns)
                of sorted patterns in non-increasing order for each snippet of
                code.
        """

        if X.ndim != 1:
            raise Exception("Only input with size 1, N is allowed")
        else:
            X = X.copy()
            X = np.expand_dims(X, axis=0)

        ranked = []
        quantity_funcs = {
            'log': lambda x: np.log1p(x) / np.log(10),
            'exp': lambda x: np.exp(x + 1),
            'linear': lambda x: x,
        }

        for snippet in X:
            try:
                item = quantity_funcs[quantity_func](snippet)
                pairs = self.__vstack_arrays(self.__get_pairs(item, th))
                pairs = pairs[pairs[:, 0].argsort()]
                ranked.append(pairs[:, 1].T.tolist()[::-1])
            except Exception:
                raise Exception("Unknown func")

        return (np.array(ranked), pairs[:, 0].T.tolist()[::-1])
