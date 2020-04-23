import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
import pickle

import pandas as pd
import torch.nn as nn
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from aibolit.config import CONFIG
from catboost import CatBoostRegressor
import lightgbm as lgbm
import numpy as np
from catboost import CatBoostClassifier, Pool, cv
from sklearn.metrics import accuracy_score

class TwoFoldRankingModel(BaseEstimator):

    def __init__(self, only_patterns, tree_method='CatBoost'):
        if tree_method not in ['CatBoost', 'RF', 'LGBM']:
            raise Exception("Unknown tree_method")
        self.tree_method = tree_method
        self.do_rename_columns = False
        self.model = None
        self.only_patterns = only_patterns

    def __read_file(
            self,
            scale_ncss=True,
            scale=False,
            **kwargs):

        df = pd.read_csv(r'C:\Users\e00533045\aibolit\scripts\target\dataset.csv')
        # print(Path(os.getcwd(), 'target', 'dataset.csv'))
        # df = pd.read_csv(str(Path(os.getcwd(), 'target', 'dataset.csv')))
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

    def fit(self):
        self.__read_file()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.input, self.target, test_size=0.3)
        # TODO cross-validation for cat boost and LGBM, find out needed parameters
        if self.tree_method == 'CatBoost':
            self.model = CatBoostRegressor(verbose=0)
            self.model.fit(self.X_train, self.y_train.ravel())
        elif self.tree_method == 'LGBM':
            self.model = lgbm.LGBMRegressor(
                learning_rate=0.01,
                n_estimators=1000
            )
            self.model.fit(self.input, self.target.ravel())
        elif self.tree_method == 'RF':
            rfc = RandomForestRegressor(random_state=42)
            param_grid = {
                'bootstrap': [True],
                'max_depth': [80, 90, 100, 110],
                'max_features': range(2, self.input.shape[1]),
                'min_samples_leaf': [3, 4, 5],
                'min_samples_split': [8, 10, 12],
                'n_estimators': [100, 200, 300, 1000]
            }

            CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5,
                   n_jobs=-1, verbose=1)
            CV_rfc.fit(self.X_train, self.y_train)
            print(CV_rfc.best_params_)
            print('Training best model')
            self.model = RandomForestClassifier(**CV_rfc.best_params_)
            self.model.fit(self.X_train, self.y_train)

    def __get_pairs(self, item):
        return item * self.model.feature_importances_, np.arange(self.model.feature_importances_.size)

    def __vstack_arrays(self, res):
        return np.vstack(res).T

    def predict(self, quantity_func='log'):
        ranked = []
        quantity_funcs = {
            'log': lambda x: np.log(x + 1),
            'exp': lambda x: np.exp(x + 1),
            'quantity_func': lambda x: x,
        }
        # code snippet -- patterns representation
        for snippet in self.X_test:
            try:
                item = quantity_funcs[quantity_func](snippet)
                pairs = self.__vstack_arrays(self.__get_pairs(item))
                pairs = pairs[pairs[:, 0].argsort()]
                ranked.append(pairs[:, 1].T.tolist()[::-1])
            except:
                raise Exception("Unknown func")


        return np.array(ranked)

    def recommend(self, snippet, display=False):
        log_q = np.log(snippet + 1)
        patterns_number = self.model.feature_importances_.size
        pairs = np.vstack((log_q * self.model.feature_importances_,
                           np.arange(patterns_number)))
        pairs = pairs.T.tolist()
        pairs.sort(reverse=True)
        pairs = list(map(lambda p: [p[0], int(p[1])], pairs))
        recommendation = self.only_patterns[pairs[0][1]]
        if display:
            print(recommendation)

        return recommendation
