import os
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import torch.nn as nn
from catboost import CatBoost
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler

from aibolit.config import CONFIG


class Maxout(nn.Module):

    def __init__(self, d_in, d_out, pool_size):
        super().__init__()
        self.d_in, self.d_out, self.pool_size = d_in, d_out, pool_size
        self.lin = nn.Linear(d_in, d_out * pool_size)

    def forward(self, inputs):
        shape = list(inputs.size())
        shape[-1] = self.d_out
        shape.append(self.pool_size)
        max_dim = len(shape) - 1
        out = self.lin(inputs)
        m, i = out.view(*shape).max(max_dim)
        return m


# this value was given during model evaluation
neurons_number = 50


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.f = nn.Sequential(
            Maxout(23, neurons_number, 2),
            Maxout(neurons_number, neurons_number, 2),
            nn.Linear(neurons_number, 1)
        )

    def forward(self, x):
        return self.f(x)


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

        # df = pd.read_csv(r'D:\git\aibolit\scripts\target\dataset.csv')
        print(Path(os.getcwd(), 'target', 'dataset.csv'))
        df = pd.read_csv(str(Path(os.getcwd(), 'target', 'dataset.csv')))
        df = df[~df["filename"].str.lower().str.contains("test")]

        if self.do_rename_columns:
            p_codes = \
                [x['code'] for x in CONFIG['patterns']] \
                + ['lines' + x['code'] for x in CONFIG['patterns']]
            m_codes = [x['code'] for x in CONFIG['metrics']]
            keys = p_codes + m_codes
            vals = \
                [x['name'] for x in CONFIG['patterns']] \
                + ['lines' + x['name'] for x in CONFIG['patterns']] \
                + [x['name'] for x in CONFIG['metrics']]

            replace_dict = dict(zip(keys, vals))
            df = df.rename(replace_dict)
            df.columns = vals
            print('Columns renamed:' + df.head())

        df = df.dropna().drop_duplicates(subset=df.columns.difference(['filename']))
        df = df[(df.ncss > 20) & (df.ncss < 100) & (df.npath_method_avg < 100000.00)].copy().reset_index()
        df.rename(columns={'for_type_cast_number': 'force_type_cast_number'}, inplace=True)

        df.drop('filename', axis=1, inplace=True)
        df.drop('index', axis=1, inplace=True)
        self.target = df[['cyclo']].copy().values
        if scale_ncss:
            new = pd.DataFrame(df[self.only_patterns].values / df['M2'].values.reshape((-1, 1)))
        else:
            new = df[self.only_patterns].copy()
        if scale:
            self.input = pd.DataFrame(StandardScaler().fit_transform(new.values), columns=new.columns,
                                      index=new.index).values
        else:
            self.input = new.values


class TwoFoldRankingModel(BaseEstimator):

    def __init__(self):
        self.do_rename_columns = False
        self.model = None

    def fit(self, X, y, display=False):
        """
        Args:
            X: np.array with shape (number of snippets, number of patterns) or
                (number of patterns, ).
            y: np.array with shape (number of snippets,), array of snippets
                complexity metric values
            display: bool, to output info about training or not
        """
        model = CatBoost()
        self.model = model
        self.model.fit(X, y.ravel())

    def __get_pairs(self, item, th: float):
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        pattern_importances = item * self.model.feature_importances_
        th_mask = (sigmoid(pattern_importances) > th) + 0
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

        if X.ndim == 1:
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

        return np.array(ranked)
