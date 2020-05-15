import os
import subprocess
from pathlib import Path
from sklearn.model_selection import train_test_split  # type: ignore
import pickle
from aibolit.model.model import Dataset, TwoFoldRankingModel  # type: ignore
from aibolit.config import Config


def collect_dataset(java_folder, max_classes=None):
    """
    Run bash scripts to collect metrics and patterns for java files

    :param java_folder: folder to java files which will be analyzed
    """

    os.chdir(Path(Config.home_aibolit_folder(), 'scripts'))
    if not java_folder:
        java_folder = Path('target/01').absolute()
        print('Analyzing {} dir:'.format(java_folder))

    print('Current working directory: ', Path(os.getcwd()))
    print('Directory with JAVA classes: ', java_folder)
    print('Filtering java files...')

    filter_cmd = ['make', 'filter']
    metrics_cmd = ['make', 'metrics']
    if java_folder is not None:
        filter_cmd.append(f'dir={java_folder}')
        metrics_cmd.append(f'dir={java_folder}')
    if max_classes is not None:
        filter_cmd.append(f'max_classes={max_classes}')

    result = subprocess.run(filter_cmd, stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stderr)
        exit(2)
    else:
        print(result.stdout)

    print('Download PMD and compute metrics...')
    result = subprocess.run(metrics_cmd, stdout=subprocess.PIPE)
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


def train_process(model_folder=None):
    """
    Define needed columns for dataset and run model training

    :param model_folder: path to model
    """
    if not model_folder:
        config = Config.get_patterns_config()
        only_patterns = [
            x['code'] for x in list(config['patterns'])
            if x['code'] not in config['patterns_exclude']
        ]
        only_metrics = \
            [x['code'] for x in list(config['metrics'])
             if x['code'] not in config['metrics_exclude']] \
            + ['halstead volume']
        columns_features = only_metrics + only_patterns
        features_number = len(columns_features)
        print("Number of features: ", features_number)

        dataset = Dataset(only_patterns)
        dataset.preprocess_file()
        features_conf = {
            "features_order": dataset.feature_order,
            "patterns_only": only_patterns
        }

        X_train, X_test, y_train, y_test = train_test_split(dataset.input, dataset.target, test_size=0.3)
        model = TwoFoldRankingModel()
        model.fit(X_train, y_train)
        model.features_conf = features_conf

        with open(Path(Config.folder_to_save_model_data(), 'model.pkl'), 'wb') as fid:
            pickle.dump(model, fid)

        print('Test loaded model:')
        with open(Path(Config.folder_to_save_model_data(), 'model.pkl'), 'rb') as fid:
            model_new = pickle.load(fid)
            preds = model_new.predict(X_test)
            print(preds)
    else:
        Exception('External models are not supported yet')
