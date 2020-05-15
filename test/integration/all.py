import os
import sys
from aibolit.config import Config

# TODO: fix all errors in the patterns/metrics and make these lists empty
EXCLUDE_PATTERNS = ['P31', 'P32']
EXCLUDE_METRICS = []

current_path: str = os.path.dirname(os.path.realpath(__file__))
for filename in os.listdir(current_path + '/samples'):

    for pattern in Config.get_patterns_config()['patterns']:
        if pattern['code'] in EXCLUDE_PATTERNS:
            continue
        try:
            path_to_file = os.path.join(current_path, 'samples', filename)
            pattern['make']().value(path_to_file)
        except Exception:
            print(
                "Error apply the pattern:",
                pattern['name'],
                pattern['code'],
                "to file",
                filename
            )
            sys.exit(1)

    for metric in Config.get_patterns_config()['metrics']:
        if metric['code'] in EXCLUDE_METRICS:
            continue
        try:
            path_to_file = os.path.join(current_path, 'samples', filename)
            metric['make']().value(path_to_file)
        except Exception:
            print(
                "Error apply the metric:",
                metric['name'],
                metric['code'],
                "to file",
                filename
            )
            sys.exit(1)

sys.exit(0)
