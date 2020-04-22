import subprocess

from aibolit.config import CONFIG
from aibolit.model.model import *
from pathlib import Path

def collect_dataset():
    """
    Run bash scripts to collect metrics and patterns for java files
    """
    cfg_path = Path(os.getcwd(), 'aibolit/cfg/cfg.json')
    print('Current working directory: ', Path(os.getcwd()))
    with open(cfg_path) as f:
        cfg = json.loads(f.read())
    os.chdir(Path(cfg['aibolit_dir'], 'scripts'))

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

def train_process(model_folder=None):
    """
    Define needed columns for dataset and run model training

    :param model_folder: path to model
    """
    if not model_folder:
        ignore_patterns = ['P27']
        ignore_metrics = ['M4', 'M5']

        only_patterns = [x['code'] for x in list(CONFIG['patterns']) if x not in ignore_patterns]
        only_metrics = [x['code'] for x in list(CONFIG['metrics']) if x not in ignore_metrics]
        columns_features = only_metrics + only_patterns
        features_number = len(columns_features)

        print("Number of features: ", features_number)
        model = SVMModel(columns_features)
        model.train()
        model.validate()
    else:
        Exception('External models are not supported yet')
