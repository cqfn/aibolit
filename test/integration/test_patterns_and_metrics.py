# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from os import listdir
from pathlib import Path
from typing import Set

import numpy as np
from tqdm import tqdm

from aibolit.config import Config
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast

# TO-FIX: fix all errors in the patterns/metrics and make these lists empty
EXCLUDE_PATTERNS: Set[str] = {}
EXCLUDE_METRICS: Set[str] = {}

# TO-FIX: refactor or delete following patterns and metrics
PATTERNS_ACCEPT_FILE_PATH = {
    "P20_5",
    "P20_7",
    "P20_11",  # P20* wasn't refactored yet
    "P28",  # patterns based on text cannot accept arbitrary AST
}
METRICS_ACCEPT_FILE_PATH = {"M1", "M3_1", "M3_2", "M3_3", "M3_4", "M5", "M7"}

samples_path = Path(__file__).absolute().parent / "samples"


def _check_pattern(p_info, filepath):
    try:
        pattern = p_info["make"]()
        if p_info["code"] in PATTERNS_ACCEPT_FILE_PATH:
            pattern_result = pattern.value(filepath)
        else:
            ast = AST.build_from_javalang(build_ast(filepath))
            pattern_result = pattern.value(ast)

        assert isinstance(pattern_result, list) and all(
            isinstance(item, int) for item in pattern_result
        ), (
            f"Pattern return {pattern_result} with type {type(pattern_result)}, "
            "but list of int was expected."
        )
    except Exception as exception:
        raise RuntimeError(
            f"Error searching for pattern {p_info['name']} "
            f"with code {p_info['code']} for file {filepath}"
        ) from exception


def _check_metric(m_info, filepath):
    try:
        metric = m_info["make"]()
        if m_info["code"] in METRICS_ACCEPT_FILE_PATH:
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
            f"Error in application of the metric {m_info['name']} "
            f"with code {m_info['code']} for file {filepath}"
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
