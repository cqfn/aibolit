import os
import shutil
import subprocess
from pathlib import Path
from sklearn.model_selection import train_test_split  # type: ignore
import pickle
from aibolit.model.model import Dataset, TwoFoldRankingModel  # type: ignore
from aibolit.config import Config


def collect_dataset(args):
    """
    Run bash scripts to collect metrics and patterns for java files
    """

    def make_patterns(args, cur_work_dir):
        print('Compute patterns...')
        result = subprocess.run(['make', 'patterns'], stdout=subprocess.PIPE, encoding='utf-8', cwd=cur_work_dir)
        print(result.returncode)
        if result.returncode != 0:
            print(result.stderr.decode())
            exit(3)
        else:
            print(result.stdout.decode())
            if args.dataset_file:
                dataset_file_path = Path(cur_work_dir, args.dataset_file)
                if not dataset_file_path.parent.exists():
                    dataset_file_path.parent.mkdir(parents=True)
                shutil.copy(Path(Config.dataset_file()), dataset_file_path)
            else:
                dataset_file_path = Config.dataset_file()
            print('dataset was saved to {}'.format(str(dataset_file_path.absolute())))


    def run_cmd(metrics_cmd, cur_work_dir):
        result = subprocess.run(metrics_cmd, stdout=subprocess.PIPE, cwd=cur_work_dir)
        if result.returncode != 0:
            print(result.stderr)
            exit(1)
        else:
            print(result.stdout.decode())

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
    metrics_cmd = ['make', 'metrics']
    merge_cmd = ['make', 'merge']
    build_halstead_cmd = ['make', 'build_halstead']
    make_hl_cmd = ['make', 'hl']

    if java_folder is not None:
        filter_cmd.append(f'dir={java_folder}')
        metrics_cmd.append(f'dir={java_folder}')
    if max_classes is not None:
        filter_cmd.append(f'max_classes={max_classes}')

    run_cmd(filter_cmd, cur_work_dir)
    print('Download PMD and compute metrics...')
    run_cmd(metrics_cmd, cur_work_dir)
    make_patterns(args, cur_work_dir)
    print('Building halstead.jar...')
    run_cmd(build_halstead_cmd, cur_work_dir)
    print('Calculating halstead metrics...')
    run_cmd(make_hl_cmd, cur_work_dir)

    print('Merge results and create dataset...')
    run_cmd(merge_cmd)


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
