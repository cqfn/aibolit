import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
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


class AbstractModel(ABC):

    @abstractmethod
    def train(self, **kwargs):
        pass

    @abstractmethod
    def read_file(
            self,
            scale_ncss=False,
            scale=False,
            **kwargs):
        pass

    @abstractmethod
    def validate(self, **kwargs):
        pass


class SVMModel(AbstractModel):

    def __init__(self, columns_features):
        super(AbstractModel)
        self.model = None
        self.columns_features = columns_features
        self.do_rename_columns = True

    def read_file(
            self,
            scale_ncss=False,
            scale=False,
            **kwargs):

        df = pd.read_csv('target/dataset.csv')
        df = df.dropna(how='any', axis=0)
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

    def train(self):

        self.read_file()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.Y,
            test_size=0.3)

        rfc = RandomForestClassifier(random_state=42)
        param_grid = {
            'n_estimators': [200, 500],
            'max_depth': [4, 5, 6, 7, 8],
            'criterion': ['gini', 'entropy']
        }

        CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=5)
        CV_rfc.fit(self.X_train, self.y_train)
        print('Best params: for a model:' + CV_rfc.best_params_)
        path_to_save = Path(os.getcwd(), 'aibolit/model')
        with open(Path(path_to_save, 'model_params.json')) as w:
            json.dump(w, CV_rfc.best_params_)
        self.best_model = RandomForestClassifier(**CV_rfc.best_params_)

    def validate(self, **kwargs):
        print('Evaluating best model...')
        self.best_model.fit(self.X_train, self.y_train)
        self.pred = self.best_model.predict(self.X_test)
        report = classification_report(self.y_test, self.pred)
        print(report)
