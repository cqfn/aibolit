# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import importlib.util
from pathlib import Path

import pandas as pd


def load_calculate_metrics_module():
    """Load the metrics script as a Python module for direct testing."""
    script_path = Path(__file__).resolve().parents[2] / 'scripts' / '03-calculate-metrics.py'
    spec = importlib.util.spec_from_file_location('calculate_metrics', script_path)
    if spec is None:
        raise RuntimeError(f'Failed to load module spec from {script_path}')
    if spec.loader is None:
        raise RuntimeError(f'Failed to load module loader from {script_path}')
    loader = spec.loader
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def test_collect_analysis_targets_includes_top_level_java_files(tmp_path):
    """Top-level Java files should be included in analysis targets."""
    module = load_calculate_metrics_module()
    root_java = tmp_path / 'TopLevel.java'
    root_java.write_text('class TopLevel {}', encoding='utf-8')

    targets = module.collect_analysis_targets(tmp_path)

    assert targets == [root_java]


def test_collect_analysis_targets_keeps_directories_and_root_java_files(tmp_path):
    """Directories and root-level Java files should both be analyzed."""
    module = load_calculate_metrics_module()
    nested_dir = tmp_path / 'project'
    nested_dir.mkdir()
    root_java = tmp_path / 'TopLevel.java'
    root_java.write_text('class TopLevel {}', encoding='utf-8')
    (tmp_path / 'README.md').write_text('ignore me', encoding='utf-8')

    targets = module.collect_analysis_targets(tmp_path)

    assert [path.name for path in targets] == ['TopLevel.java', 'project']


def test_aggregate_method_metric_ignores_class_rows():
    """Method metric aggregation should skip class-level PMD rows."""
    module = load_calculate_metrics_module()
    frame = pd.DataFrame({
        'File': ['Book.java', 'Book.java', 'Book.java'],
        'class': [0, 0, 1],
        'cyclo': [2.0, 4.0, 100.0],
    })

    metrics = module.aggregate_method_metric(
        frame,
        'cyclo',
        'mean',
        'cyclo_method_avg',
    )

    assert metrics.to_dict('index') == {'Book.java': {'cyclo_method_avg': 3.0}}
