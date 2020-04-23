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

class TwoFoldRankingModel(BaseEstimator):

    def __init__(self, columns_features, only_patterns, tree_method='CatBoost'):
        if tree_method not in ['CatBoost', 'RF', 'LGBM']:
            raise Exception("Unknown tree_method")
        self.tree_method = tree_method
        self.do_rename_columns = False
        self.importances = None
        self.model = None
        self.columns_features = columns_features
        self.only_patterns = only_patterns

    def read_file(
            self,
            scale_ncss=False,
            scale=False,
            **kwargs):

        # df = pd.read_csv(r'C:\Users\e00533045\aibolit\scripts\target\dataset.csv')
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
        self.Y = df[['cyclo']].copy().values
        if scale_ncss:
            new = pd.DataFrame(df[self.columns_features].values / df['ncss_lightweight'].values.reshape((-1, 1)))
        else:
            new = df[self.columns_features].copy()
        if scale:
            self.X = pd.DataFrame(StandardScaler().fit_transform(new.values), columns=new.columns,
                                  index=new.index).values
        else:
            self.X = new.values

    def fit(self):
        if self.tree_method == 'CatBoost':
            self.model = CatBoostRegressor(verbose=0)
            self.model.fit(self.X, self.Y.ravel())
        elif self.tree_method == 'LGBM':
            self.model = lgbm.LGBMRegressor(
                learning_rate=0.01,
                n_estimators=1000
            )
            self.model.fit(self.X, self.Y.ravel())
        elif self.tree_method == 'RF':
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y.values, test_size=0.3)
            rfc = RandomForestClassifier(random_state=42)
            param_grid = {
                'n_estimators': [200, 500],
                'max_depth': [4, 5, 6, 7, 8],
                'criterion': ['gini', 'entropy']
            }

            CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
            CV_rfc.fit(X_train, y_train)
            print(CV_rfc.best_params_)
            print('Training best model')
            self.model = RandomForestClassifier(**CV_rfc.best_params_)
            self.model.fit(X_train, y_train)
            print('Evaluating best model...')
            self.pred = self.model.predict(X_test)
            report = classification_report(y_test, self.pred)
            print(report)

        with open(Path(os.getcwd(), 'aibolit', 'binary_files', 'my_dumped_classifier.pkl'), 'wb') as fid:
            pickle.dump(self.model, fid)

        self.importances = self.model.feature_importances_

    def __get_pairs(self, item):
        return item * self.importances, np.arange(self.importances.size)

    def __vstack_arrays(self, res):
        return np.vstack(res).T

    def predict(self, X, quantity_func='log'):
        ranked = []
        quantity_funcs = {
            'log': lambda x: np.log(x + 1),
            'exp': lambda x: np.exp(x + 1),
            'quantity_func': lambda x: x,
        }
        # code snippet -- patterns representation
        for snippet in X:
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
        patterns_number = self.importances.size
        pairs = np.vstack((log_q * self.importances,
                           np.arange(patterns_number)))
        pairs = pairs.T.tolist()
        pairs.sort(reverse=True)
        pairs = list(map(lambda p: [p[0], int(p[1])], pairs))
        recommendation = self.only_patterns[pairs[0][1]]
        if display:
            print(recommendation)

        return recommendation

# def train(self):
#
#     self.read_file()
#     self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
#         self.X,
#         self.Y,
#         test_size=0.3)
#
#     rfc = RandomForestClassifier(random_state=42)
#     param_grid = {
#         'n_estimators': [200, 500],
#         'max_depth': [4, 5, 6, 7, 8],
#         'criterion': ['gini', 'entropy']
#     }
#
#     CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
#     CV_rfc.fit(self.X_train, self.y_train)
#     print('Best params: for a model:' + str(CV_rfc.best_params_))
#     path_to_save = Path(Path(os.getcwd()).parent, 'aibolit', 'binary_files')
#     with open(Path(path_to_save, 'model_params.json'), 'w') as w:
#         json.dump(w, CV_rfc.best_params_)
#     self.best_model = RandomForestClassifier(**CV_rfc.best_params_)

# def validate(self, **kwargs):
#     print('Evaluating best model...')
#     self.best_model.fit(self.X_train, self.y_train)
#     self.pred = self.best_model.predict(self.X_test)
#     report = classification_report(self.y_test, self.pred)
#     print(report)
#
#     # save the classifier
#     with open(Path(os.getcwd(), 'aibolit', 'binary_files', 'my_dumped_classifier.pkl'), 'wb') as fid:
#         pickle.dump(self.best_model, fid)