# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import inspect

from aibolit.ast_framework.ast import AST
from aibolit.config import Config


def test_each_metric_in_config_accepts_ast():
    patterns_config = Config.get_patterns_config()
    metrics_exclude = set(patterns_config.get('metrics_exclude', []))
    for metric_config in patterns_config['metrics']:
        if metric_config['code'] in metrics_exclude:
            continue
        metric = metric_config['make']()
        metric_signature = inspect.signature(metric.value)
        assert 'ast' in metric_signature.parameters
        ann = metric_signature.parameters['ast'].annotation
        assert is_ast_or_subclass(ann), (
            f"{metric_config['name']} "
            f"metric.value 'ast' parameter should be typed as AST or subclass"
        )


def is_ast_or_subclass(ann):
    if ann is inspect.Signature.empty:
        return False
    if isinstance(ann, str):
        return ann == 'AST'
    try:
        return issubclass(ann, AST)
    except TypeError:
        return False


def test_each_pattern_in_config_accepts_ast():
    patterns_config = Config.get_patterns_config()
    for pattern_config in patterns_config['patterns']:
        pattern = pattern_config['make']()
        pattern_signature = inspect.signature(pattern.value)
        assert 'ast' in pattern_signature.parameters
        assert pattern_signature.parameters['ast'].annotation is AST


def test_ncss_metric_in_config_accepts_ast():
    patterns_config = Config.get_patterns_config()
    metric_config = next(
        mc for mc in patterns_config['metrics'] if mc['name'] == 'NCSS lightweight'
    )
    metric = metric_config['make']()
    metric_signature = inspect.signature(metric.value)
    assert 'ast' in metric_signature.parameters
    assert metric_signature.parameters['ast'].annotation is AST


def test_asserts_pattern_in_config_accepts_ast():
    patterns_config = Config.get_patterns_config()
    pattern_config = next(pt for pt in patterns_config['patterns'] if pt['name'] == 'Asserts')
    pattern = pattern_config['make']()
    pattern_signature = inspect.signature(pattern.value)
    assert 'ast' in pattern_signature.parameters
    assert pattern_signature.parameters['ast'].annotation is AST
