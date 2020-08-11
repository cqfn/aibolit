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

from os import listdir
from pathlib import Path
from typing import Set

import numpy as np
from tqdm import tqdm

from aibolit.config import Config
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast

# TODO: fix all errors in the patterns/metrics and make these lists empty
EXCLUDE_PATTERNS: Set[str] = {}
EXCLUDE_METRICS: Set[str] = {}

# TODO: refactor or delete following patterns and metrics
PATTERNS_ACCEPT_FILE_PATH = {
    "P20_5",
    "P20_7",
    "P20_11",  # P20* wasn't refactored yet
    "P28",  # patterns based on text cannot accept arbitrary AST
}
METRICS_ACCEPT_FILE_PATH = {"M1", "M3_1", "M3_2", "M3_3", "M3_4", "M4", "M5", "M6", "M7"}

samples_path = Path(__file__).absolute().parent / "samples"


def _check_pattern(pattern_info, filepath):
    try:
        pattern = pattern_info["make"]()
        if pattern_info["code"] in PATTERNS_ACCEPT_FILE_PATH:
            pattern_result = pattern.value(filepath)
        else:
            ast = AST.build_from_javalang(build_ast(filepath))
            pattern_result = pattern.value(ast)

        assert isinstance(pattern_result, list) and all(
            isinstance(item, int) for item in pattern_result
        ), f"Pattern return {pattern_result} with type {type(pattern_result)}, but list of int was expected."
    except Exception as exception:
        raise RuntimeError(
            f"Error searching for pattern {pattern_info['name']} "
            f"with code {pattern_info['code']} for file {filepath}"
        ) from exception


def _check_metric(metric_info, filepath):
    try:
        metric = metric_info["make"]()
        if metric_info["code"] in METRICS_ACCEPT_FILE_PATH:
            metric_result = metric.value(filepath)
        else:
            ast = AST.build_from_javalang(build_ast(filepath))
            metric_result = metric.value(ast)

        assert isinstance(metric_result, (int, float, np.float64)), (
            f"Metric return {metric_result} of type {type(metric_result)}, "
            "but int, float or numpy float was expected"
        )
    except Exception as exception:
        raise RuntimeError(
            f"Error in application of the metric {metric['name']} "
            f"with code {metric['code']} for file {filename}"
        ) from exception


if __name__ == "__main__":
    config = Config.get_patterns_config()

    print(f"Processed files in {samples_path}:")
    for filename in tqdm(listdir(samples_path)):
        for pattern_info in config["patterns"]:
            if pattern_info["code"] not in EXCLUDE_PATTERNS:
                _check_pattern(pattern_info, samples_path / filename)

        for metric_info in config["metrics"]:
            if metric_info["code"] not in EXCLUDE_METRICS:
                _check_metric(metric_info, samples_path / filename)
