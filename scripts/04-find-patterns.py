# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from argparse import ArgumentParser
from collections import defaultdict
from concurrent.futures import TimeoutError
from csv import DictWriter, QUOTE_MINIMAL
from functools import partial
from logging import basicConfig, INFO, warning
from os import cpu_count, getenv, makedirs
try:
    from os import sched_getaffinity
except ImportError:
    MAYBE_ON_MACOS = True
else:
    MAYBE_ON_MACOS = False
from pathlib import Path
from sys import stderr
from typing import Any, Dict, List
import json

from pebble import ProcessPool
from tqdm import tqdm

from aibolit.config import Config
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.utils.ast_builder import build_ast


class FileProcessingError(RuntimeError):
    def __init__(self, filepath: str, pattern_name: str, cause: Exception):
        super().__init__(f'Failed calculating {pattern_name} on file {filepath}.\nReason: {cause}')

        self.filepath = filepath
        self.pattern_name = pattern_name
        self.cause = cause


def _calculate_patterns_and_metrics(
    file_path: str, is_decomposition_requested: bool
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    config = Config.get_patterns_config()
    patterns_info = [
        pattern_info
        for pattern_info in config['patterns']
        if pattern_info['code'] not in config['patterns_exclude']
    ]

    metrics_info = [
        metric_info
        for metric_info in config['metrics']
        if metric_info['code'] not in config['metrics_exclude']
    ]

    ast = AST.build_from_javalang(build_ast(file_path))
    classes_ast = [
        ast.subtree(node)
        for node in ast.root().types
        if node.node_type == ASTNodeType.CLASS_DECLARATION
    ]

    for class_ast in classes_ast:
        components = (
            decompose_java_class(class_ast, 'strong', ignore_getters=True, ignore_setters=True)
            if is_decomposition_requested
            else [class_ast]
        )
        for index, component_ast in enumerate(components):
            calculation_result = {
                'filepath': file_path,
                'class_name': class_ast.root().name,
                'component_index': index,
            }

            for pattern_info in patterns_info:
                try:
                    pattern = pattern_info['make']()
                    pattern_result = pattern.value(component_ast)
                    calculation_result[pattern_info['code']] = len(pattern_result)
                    calculation_result['lines_' + pattern_info['code']] = pattern_result
                except Exception as cause:
                    raise FileProcessingError(file_path, pattern_info['name'], cause)

            for metric_info in metrics_info:
                try:
                    metric = metric_info['make']()
                    metric_result = metric.value(component_ast)
                    calculation_result[metric_info['code']] = metric_result
                except Exception as cause:
                    raise FileProcessingError(file_path, metric_info['name'], cause)

            results.append(calculation_result)

    return results


def _create_dataset_writer(file):
    config = Config.get_patterns_config()

    patterns_codes = [
        pattern['code'] for pattern in config['patterns']
        if pattern['code'] not in config['patterns_exclude']
    ]

    metrics_codes = [
        metric['code'] for metric in config['metrics']
        if metric['code'] not in config['metrics_exclude']
    ]

    fields = \
        patterns_codes + \
        metrics_codes + \
        ['lines_' + code for code in patterns_codes] + \
        ['filepath', 'class_name', 'component_index']

    return DictWriter(file, delimiter=';', quotechar='"', quoting=QUOTE_MINIMAL, fieldnames=fields)


def _parse_args():
    allowed_cores_qty = _allowed_cores_qty()
    system_cores_qty = _system_cores_qty()

    parser = ArgumentParser(description='Creates dataset')
    parser.add_argument('file', help='Path for file with a list of Java files.')

    parser.add_argument(
        '--jobs',
        '-j',
        type=int,
        default=min(allowed_cores_qty, system_cores_qty),
        help='Number of processes to spawn. '
        'By default one less than number of cores. '
        'Be carefull to raise it above, machine may stop responding while creating dataset.',
    )

    parser.add_argument(
        '--timeout',
        '-t',
        type=float,
        default=60,
        help='Maximum time (in seconds) for single file proccessing. Default is 60 seconds. '
        'If 0, no timeout is set.',
    )

    parser.add_argument(
        '--log',
        '-l',
        default='pattern_calculation.log',
        help='Path for log file. pattern_calculation.log is default.',
    )

    parser.add_argument(
        '--errors-log',
        '-el',
        default='calculation_errors.json',
        help='Path for errors log file. All errors grouped by patterns. '
             'calculation_errors.log is default.',
    )

    parsed_args = parser.parse_args()

    if parsed_args.jobs >= system_cores_qty:
        print(
            f'WARNING: You have ordered to spawn {parsed_args.jobs} jobs, '
            f'while system has only {system_cores_qty} cores. '
            'Machine may badly respond, while calculating dataset.',
            file=stderr,
        )

    if parsed_args.jobs > allowed_cores_qty:
        print(
            f'WARNING: You have ordered to spawn {parsed_args.jobs} jobs, '
            f'while process only allowed to occupy {allowed_cores_qty} cores.'
            'You may have a slowdown due to large number of processes.',
            file=stderr,
        )

    if parsed_args.timeout == 0:
        parsed_args.timeout = None

    basicConfig(filename=parsed_args.log, filemode='w', level=INFO)

    default_dataset_directory = Path('.', 'target', '04').absolute()
    dataset_directory = Path(getenv('TARGET_FOLDER') or default_dataset_directory)
    makedirs(dataset_directory, exist_ok=True)
    parsed_args.csv_file = Path(dataset_directory, '04-find-patterns.csv')

    is_decomposition_requested = getenv('LCOM_DECOMPOSITION', 'True')
    if is_decomposition_requested in {'True', '1'}:
        parsed_args.is_decomposition_requested = True
    elif is_decomposition_requested in {'False', '0'}:
        parsed_args.is_decomposition_requested = False
    else:
        print(
            f"WARNING: value of 'LCOM_DECOMPOSITION' environment variable "
            f"{is_decomposition_requested} is not recognized. "
            "Available options are 'True', 'False', '1', '0'. "
            "Decomposition is applied by default.",
            file=stderr,
        )
        parsed_args.is_decomposition_requested = True

    return parsed_args


def _allowed_cores_qty() -> int:
    return len(sched_getaffinity(0)) if not MAYBE_ON_MACOS else _cpu_count()


def _system_cores_qty() -> int:
    return _cpu_count()


def _cpu_count() -> int:
    num = cpu_count()
    if num is not None:
        # if None, then the number of CPUs is undeterminable
        return num
    return 1  # fallback


if __name__ == '__main__':
    args = _parse_args()

    errors: List[FileProcessingError] = []
    timeout_errors_qty = 0
    parsing_errors_qty = 0

    calculate_patterns_and_metrics = partial(
        _calculate_patterns_and_metrics, is_decomposition_requested=args.is_decomposition_requested
    )

    with (open(args.file, encoding='utf-8') as input,
          open(args.csv_file, 'w', encoding='utf-8') as output,
          ProcessPool(args.jobs) as executor):
        dataset_writer = _create_dataset_writer(output)
        dataset_writer.writeheader()

        filenames = [filename.rstrip() for filename in input.readlines()]
        future = executor.map(calculate_patterns_and_metrics, filenames, timeout=args.timeout,)
        dataset_features = future.result()

        for filename in tqdm(filenames):
            try:
                single_file_features = next(
                    dataset_features)
                dataset_writer.writerows(single_file_features)
            except TimeoutError:
                warning(f'Processing {filename} is aborted due to '
                        f'timeout in {args.timeout} seconds.')
                timeout_errors_qty += 1
            except Exception as e:
                warning(e)
                parsing_errors_qty += 1
                if isinstance(e, FileProcessingError):
                    errors.append(e)

    if timeout_errors_qty or parsing_errors_qty:
        print(
            f'WARNING: There was {timeout_errors_qty} timeouts and '
            f'{parsing_errors_qty} errors during file processing.\n'
            f'Check {args.log} for detailed information.',
            file=stderr,
        )

    if len(errors) > 0:
        errors_by_pattern = defaultdict(dict)
        for error in errors:
            errors_by_pattern[error.pattern_name][error.filepath] = str(error.cause)

        with open(args.errors_log, 'w', encoding='utf-8') as errors_log:
            json.dump(errors_by_pattern, errors_log)

        print(
            f'WARNING: All errors grouped by pattern/metric name ind written to {args.errors_log}',
            file=stderr,
        )
