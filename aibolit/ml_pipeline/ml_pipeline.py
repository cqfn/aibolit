import os
import shutil
import subprocess
from pathlib import Path
import pickle
from aibolit.model.model import PatternRankingModel, scale_dataset  # type: ignore
from aibolit.config import Config
import pandas as pd  # type: ignore


def collect_dataset(args):
    """
    Run bash scripts to collect metrics and patterns for java files
    """

    def make_patterns(args, cur_work_dir):
        print('Compute patterns...')
        result = subprocess.run(['make', 'patterns'], stdout=subprocess.PIPE, encoding='utf-8', cwd=cur_work_dir)
        print(result.returncode)
        if result.returncode != 0:
            print(result.stderr)
            exit(3)
        else:
            print(result.stdout)
            if args.dataset_file:
                dataset_file_path = Path(cur_work_dir, args.dataset_file)
                if not dataset_file_path.parent.exists():
                    dataset_file_path.parent.mkdir(parents=True)
                shutil.copy(Path(Config.dataset_file()), dataset_file_path)
            else:
                dataset_file_path = Path(Config.dataset_file())
            print('dataset was saved to {}'.format(str(dataset_file_path.absolute())))

    def run_cmd(metrics_cmd, cur_work_dir):
        result = subprocess.run(metrics_cmd, stdout=subprocess.PIPE, encoding='utf-8', cwd=cur_work_dir)
        if result.returncode != 0:
            print(result.stderr)
            exit(1)
        else:
            print(result.stdout)

    # path to java files which will be analyzed
    java_folder = args.java_folder
    max_classes = args.max_classes
    os.chdir(Path(Config.home_aibolit_folder(), 'scripts'))
    if not java_folder:
        java_folder = Path('target/01').absolute()
        print('Analyzing {} dir:'.format(java_folder))
    cur_work_dir = Path(os.getcwd())
    print('Current working directory: ', cur_work_dir)
    print('Directory with JAVA classes: ', java_folder)
    print('Filtering java files...')

    filter_cmd = ['make', 'filter']
    merge_cmd = ['make', 'merge']
    split_cmd = ['make', 'split']

    if java_folder is not None:
        filter_cmd.append(f'dir={java_folder}')
    if max_classes is not None:
        filter_cmd.append(f'max_classes={max_classes}')

    run_cmd(filter_cmd, cur_work_dir)
    make_patterns(args, cur_work_dir)

    print('Merge results...')
    run_cmd(merge_cmd, cur_work_dir)

    print('Preprocess dataset, create train and test...')
    run_cmd(split_cmd, cur_work_dir)


def train_process():
    """
    Define needed columns for dataset and run model training
    """
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
    print("General number of features in config: ", features_number)

    train_dataset = pd.read_csv(Config.train_csv(), index_col=None)
    model = PatternRankingModel()
    # At the moment we use use patterns as features,
    # but in future features can be also some metrics.
    # We should differ them for any purpose (scaling, etc.)
    features_conf = {
        "features_order": only_patterns,
        "patterns_only": only_patterns
    }
    model.features_conf = features_conf
    print('Scaling features...')
    scaled_dataset = scale_dataset(train_dataset, model.features_conf)
    dataset = scaled_dataset[only_patterns]
    print('Training model...')
    model.fit_regressor(dataset, scaled_dataset['M4'])

    save_model_file = Path(Config.folder_to_save_model_data(), 'model.pkl')
    print('Saving model to loaded model from file {}:'.format(save_model_file))
    with open(save_model_file, 'wb') as fid:
        pickle.dump(model, fid)

    load_model_file = Path(Config.folder_to_save_model_data(), 'model.pkl')
    print('Test loaded model from file {}:'.format(load_model_file))
    test_dataset = pd.read_csv(Config.test_csv(), index_col=None)
    with open(load_model_file, 'rb') as fid:
        model_new = pickle.load(fid)
        scaled_test_dataset = scale_dataset(test_dataset, model_new.features_conf).sample(n=10, random_state=17)
        print('Model has been loaded successfully')
        # add ncss, ncss is needed in informative as a  last column
        X_test = scaled_test_dataset[only_patterns + ['M2']]

        for _, row in X_test.iterrows():
            preds, importances = model_new.rank(row.values)
            print(preds)
    path_with_logs = Path(os.getcwd(), 'catboost_info')
    print('Removing path with catboost logs {}'.format(path_with_logs))
    if path_with_logs.exists():
        shutil.rmtree(path_with_logs)
