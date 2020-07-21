import os
import sys
import numpy as np
from aibolit.config import Config
import tqdm
from pathlib import Path
import glob

# TODO: fix all errors in the patterns/metrics and make these lists empty
EXCLUDE_PATTERNS = []
EXCLUDE_METRICS = []

current_path: str = os.path.dirname(os.path.realpath(__file__))
print('Processed files in testing:')

for filename in tqdm.tqdm(os.listdir(current_path + '/samples')):
    for pattern in Config.get_patterns_config()['patterns']:
        if pattern['code'] in EXCLUDE_PATTERNS:
            continue
        try:
            path_to_file = os.path.join(current_path, 'samples', filename)
            patter_result = pattern['make']().value(path_to_file)
            assert isinstance(patter_result, list) and \
                all(isinstance(item, int) for item in patter_result), \
                f'Pattern return {patter_result} with type {type(patter_result)}, but list of int was expected.'
        except Exception as e:
            print(f'Error in application of the pattern "{pattern["name"]}" '
                  f'with code {pattern["code"]} for file "{filename}"')
            print(f'Reason: {e}')
            sys.exit(1)
    print(4)
    for metric in Config.get_patterns_config()['metrics']:
        if metric['code'] in EXCLUDE_METRICS:
            continue
        try:
            path_to_file = os.path.join(current_path, 'samples', filename)
            metric_result = metric['make']().value(path_to_file)
            assert isinstance(metric_result, (int, float, np.float64)), \
                f'Metric return {metric_result} of type {type(metric_result)}, ' \
                'but int, float or numpy float was expected'
        except Exception as e:
            print(f'Error in application of the metric "{metric["name"]}" '
                  f'with code {metric["code"]} for file "{filename}"')
            print(f'Reason: {e}')
            sys.exit(1)

sys.exit(0)
