import subprocess

from aibolit.config import CONFIG
from aibolit.model.model import *
from pathlib import Path

def collect_dataset():
    """
    Run bash scripts to collect metrics and patterns for java files
    """

    home = Path(Path.home(), 'aibolit\scripts')
    os.chdir(home)

    result = subprocess.run(['make', 'clean'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout)
        exit(1)

    result = subprocess.run(['make', 'metrics'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout)
        exit(2)

    result = subprocess.run(['make', 'patterns'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout)
        exit(3)

    result = subprocess.run(['make', 'build_halstead'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout)
        exit(4)

    result = subprocess.run(['make', 'hl'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout)
        exit(5)

    result = subprocess.run(['make', 'merge'], stdout=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout)
        exit(6)


def train_process(model_folder=None):
    """
    Define needed columns for dataset and run model training

    :param model_folder: path to model
    """
    if not model_folder:
        ignore_patterns = ['P27']
        ignore_metrics = ['M4', 'M5']

        only_patterns = [x for x in list(CONFIG['patterns'].keys()) if x not in ignore_patterns]
        only_metrics = [x for x in list(CONFIG['metrics'].keys()) if x not in ignore_metrics]
        columns_features = only_metrics + only_patterns
        features_number = len(columns_features)

        print("Number of features: ", features_number)
        model = SVMModel(columns_features)
        model.train()
    else:
        Exception('External models are not supported yet')
