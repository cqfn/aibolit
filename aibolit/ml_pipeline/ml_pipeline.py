import os
import subprocess
from pathlib import Path

from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score  # type: ignore
import pickle
import numpy as np  # type: ignore

from aibolit.model.model import Dataset, TwoFoldRankingModel  # type: ignore
from aibolit.config import CONFIG
import json


def collect_dataset():
    """
    Run bash scripts to collect metrics and patterns for java files
    """
    os.chdir(Path('/home/jovyan/aibolit', 'scripts'))

    print('Current working directory: ', Path(os.getcwd()))

    print('Filtering java files...')
    result = subprocess.run(['make', 'filter'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr)
        exit(2)
    else:
        print(result.stdout)

    print('Download PMD and compute metrics...')
    result = subprocess.run(['make', 'metrics'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr)
        exit(2)
    else:
        print(result.stdout)

    print('Compute patterns...')
    result = subprocess.run(['make', 'patterns'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr)
        exit(3)
    else:
        print(result.stdout)

    print('Build halstead jar...')
    result = subprocess.run(['make', 'build_halstead'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr)
        exit(4)
    else:
        print(result.stdout)

    print('Run halstead jar...')
    result = subprocess.run(['make', 'hl'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr)
        exit(5)
    else:
        print(result.stdout)

    print('Merge results and create dataset...')
    result = subprocess.run(['make', 'merge'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr)
        exit(6)
    else:
        print(result.stdout)


def mean_absolute_percentage_error(y_true, y_pred):
    y_true = np.array(y_true).reshape(-1)
    y_pred = np.array(y_pred).reshape(-1)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def print_scores(y_test, y_pred):
    print('MSE: ', mean_squared_error(y_test, y_pred))
    print('MAE: ', mean_absolute_error(y_test, y_pred))
    print('MAPE:', mean_absolute_percentage_error(y_test, y_pred))
    print('R2:  ', r2_score(y_test, y_pred))
    print('VAR:  ', np.var(y_test))


def train_process(model_folder=None):
    """
    Define needed columns for dataset and run model training

    :param model_folder: path to model
    """
    if not model_folder:
        ignore_patterns = ['P27']
        ignore_metrics = ['M4', 'M5']

        only_patterns = [x['code'] for x in list(CONFIG['patterns']) if x['code'] not in ignore_patterns]
        only_metrics = \
            [x['code'] for x in list(CONFIG['metrics']) if x['code'] not in ignore_metrics] \
            + ['halstead volume']
        columns_features = only_metrics + only_patterns
        features_number = len(columns_features)
        print("Number of features: ", features_number)

        dataset = Dataset(only_patterns)
        dataset.preprocess_file()
        cwd = Path(os.getcwd())
        features_conf = {
            "features_order": dataset.feature_order,
            "patterns_only": only_patterns
        }
        with open(r'D:\git\aibolit\aibolit\binary_files\features_order.json', 'w') as fid:
        # with open(Path(cwd.parent, 'aibolit', 'binary_files', 'features_order.json'), 'wb') as fid:
            json.dump(features_conf, fid, sort_keys=True, indent=4)

        X_train, X_test, y_train, y_test = train_test_split(dataset.input, dataset.target, test_size=0.3)
        model = TwoFoldRankingModel()
        model.fit(X_train, y_train)

        print('Cur cwd: ' + str(cwd))
        with open(Path(cwd.parent, 'aibolit', 'binary_files', 'model.pkl'), 'wb') as fid:
            pickle.dump(model, fid)

        print('Test loaded file cwd: ' + str(cwd))
        with open(Path(cwd.parent, 'aibolit', 'binary_files', 'model.pkl'), 'rb') as fid:
            model_new = pickle.load(fid)
            preds = model_new.predict(X_test)
            print(preds)
    else:
        Exception('External models are not supported yet')
