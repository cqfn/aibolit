import os
import sys
from aibolit.config import CONFIG


current_path: str = os.path.dirname(os.path.realpath(__file__))
for filename in os.listdir(current_path + '/samples'):

    for pattern in CONFIG['patterns']:
        try:
            path_to_file = os.path.join(current_path, 'samples', filename)
            pattern['make']().value(path_to_file)
        except Exception:
            print(
                "Error apply the pattern:",
                pattern['name'],
                "to file",
                filename
            )
            sys.exit(1)

    for metric in CONFIG['metrics']:
        try:
            path_to_file = os.path.join(current_path, 'samples', filename)
            metric['make']().value(path_to_file)
        except Exception:
            print(
                "Error apply the metric:",
                metric['name'],
                "to file",
                filename
            )
            sys.exit(1)

sys.exit(0)
