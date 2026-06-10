# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import inspect
import pytest

from aibolit.ast_framework.ast import AST
from aibolit.config import Config


@pytest.mark.xfail
def test_each_metric_in_config_accepts_ast():
    '''
    TODO #813:30min/DEV Ensure All Metrics Accept `ast: AST` Parameter with Type Hints
    Verify that all metrics in the config accept an AST parameter with proper type hints.
    Probable solutions:
    1. Every metric factory in patterns_config["metrics"] produces a metric with:
       - A parameter named "ast" in its call signature
       - The "ast" parameter properly annotated as `aibolit.ast_framework.ast.AST` or a subclass
    2. Remove any metrics that cannot comply with this interface.
    Once all metrics meet requirements, remove the decorator.
    '''
    patterns_config = Config.get_patterns_config()
    for metric_config in patterns_config['metrics']:
        metric = metric_config['make']()
        metric_signature = inspect.signature(metric.value)
        assert 'ast' in metric_signature.parameters
        assert metric_signature.parameters['ast'].annotation is AST


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
