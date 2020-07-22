# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
from typing import List

import numpy as np
import tqdm

from aibolit.config import Config

# TODO: fix all errors in the patterns/metrics and make these lists empty
EXCLUDE_PATTERNS: List[str] = []
EXCLUDE_METRICS: List[str] = []

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
