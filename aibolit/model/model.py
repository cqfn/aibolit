import torch.nn as nn
import torch
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.data as Data
import json
import matplotlib.pyplot as plt
from sklearn.metrics import make_scorer, classification_report, confusion_matrix
import numpy as np
import pandas as pd
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge, HuberRegressor
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, \
    explained_variance_score, mean_squared_log_error, mean_tweedie_deviance
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn import datasets, linear_model
from scipy import stats
from sklearn.pipeline import Pipeline
from sklearn.base import clone
import pandas as pd
from sklearn.preprocessing import StandardScaler
import torch.optim as optim
from sklearn.metrics import make_scorer
from typing import Set, Dict, List
from abc import ABC, abstractmethod


class AbstractModel(ABC):

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def read_file(
            self,
            columns_features,
            only_patterns,
            scale_ncss=False,
            scale=False):
        pass

    @abstractmethod
    def validate(self):
        pass


class SVMModel(AbstractModel):

    def __init__(self, FEATURES_NUMBER, ONLY_PATTERNS):
        super(AbstractModel)
        self.model = None
        self.FEATURES_NUMBER = FEATURES_NUMBER
        self.ONLY_PATTERNS = ONLY_PATTERNS

    def read_file(
            self,
            columns_features: List[str],
            only_patterns: List[str],
            scale_ncss=False,
            scale=False):

        df = pd.read_csv('dataset.csv')
        # TODO DROP ALL NULLS
        # TODO replace p23 with names
        df = df.dropna().drop_duplicates(subset=df.columns.difference(['filename']))
        df = df[(df.ncss > 20) & (df.ncss < 100) & (df.npath_method_avg < 100000.00)].copy().reset_index()
        df.rename(columns={'for_type_cast_number': 'force_type_cast_number'}, inplace=True)
        df = df[~df["filename"].str.lower().str.contains("test")]
        df.drop('filename', axis=1, inplace=True)
        df.drop('index', axis=1, inplace=True)
        self.Y = df[['cyclo']].copy().values
        self._columns = columns_features
        if scale_ncss:
            # TODO fix ncss_lightweight with patterns
            new = pd.DataFrame(df[only_patterns].values / df['ncss_lightweight'].values.reshape((-1, 1)))
        else:
            new = df[only_patterns].copy()
        if scale:
            self.X = pd.DataFrame(StandardScaler().fit_transform(new.values), columns=new.columns,
                                  index=new.index).values
        else:
            self.X = new.values

    def train(self):

        self.read_file(self.FEATURES_NUMBER, self.ONLY_PATTERNS)
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
        print(CV_rfc.best_params_)
        print('Training best model')

        rfc1 = RandomForestClassifier(**CV_rfc.best_params_)
        rfc1.fit(self.X_train, self.y_train)
        self.pred = rfc1.predict(self.X_test)
        report = classification_report(self.y_test, self.pred)
        print(report)
