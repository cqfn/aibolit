import subprocess
import os
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.data as Data
from aibolit.model.model import *
import matplotlib.pyplot as plt

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
from sklearn.ensemble import RandomForestRegressor
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


def collect_dataset(java_folder):
    # go to scripts
    os.chdir('../scripts')
    'make clean'
    'make filter'
    'make metrics'
    'make patterns'
    'make rs'
    'make build_halstead'
    'make hl'
    'make merge'


def train_process(model_folder=None):
    if not model_folder:
        from aibolit.model.model import Net, Maxout
        from aibolit import config

        COLUMNS_FEATURES = [
            'var_middle_number', 'this_find_number',
            'string_concat_number', 'instance_of_number',
            'method_chain_number', 'var_decl_diff_number_11',
            'var_decl_diff_number_7', 'var_decl_diff_number_5',
            'super_method_call_number', 'force_type_cast_number',
            'entropy', 'halstead volume', 'ncss_lightweight',
            'left_spaces_var', 'right_spaces_var', 'max_left_diff_spaces',
            'max_right_diff_spaces', 'asserts_number', 'setter_number',
            'empty_rethrow_number', 'prohibited_class_names_number',
            'return_in_if_number', 'impl_multi_number',
            'many_prim_ctors_number', 'multiple_try_number',
            'non_final_field_number', 'null_check_number',
            'part_sync_number', 'red_catch_number',
            'return_null_number'
        ]

        ONLY_PATTERNS = ['var_middle_number', 'this_find_number', 'string_concat_number', 'instance_of_number',
                         'method_chain_number', 'var_decl_diff_number_11', 'var_decl_diff_number_7',
                         'var_decl_diff_number_5',
                         'super_method_call_number', 'force_type_cast_number', 'asserts_number', 'setter_number',
                         'empty_rethrow_number',
                         'prohibited_class_names_number', 'return_in_if_number', 'impl_multi_number',
                         'many_prim_ctors_number', 'multiple_try_number', 'non_final_field_number', 'null_check_number',
                         'part_sync_number', 'red_catch_number', 'return_null_number']

        FEATURES_NUMBER = len(ONLY_PATTERNS)

        print("Number of features: ", FEATURES_NUMBER)
        model = SVMModel(FEATURES_NUMBER, ONLY_PATTERNS)
        model.train()

    else:
        Exception('External models are not supported yet')
