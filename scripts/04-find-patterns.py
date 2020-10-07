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

from argparse import ArgumentParser
from collections import defaultdict
from concurrent.futures import TimeoutError
from csv import DictWriter, QUOTE_MINIMAL
from functools import partial
from logging import basicConfig, INFO, warning
from os import cpu_count, getenv, makedirs, sched_getaffinity
from pathlib import Path
from sys import stderr
from typing import Any, Dict, List
import json
from multiprocessing import Pool

from pebble import ProcessPool
from tqdm import tqdm

from aibolit.config import Config
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.utils.ast_builder import build_ast


class FileProcessingError(RuntimeError):
    def __init__(self, filepath: str, pattern_name: str, cause: Exception):
        super().__init__(f"Failed calculating {pattern_name} on file {filepath}.\nReason: {cause}")

        self.filepath = filepath
        self.pattern_name = pattern_name
        self.cause = cause

def get_unneeded_patterns(patterns_list, patterns_filepath):
    all_patterns = set([x['code'] for x in patterns_list])

    with open(patterns_filepath) as f:
        include_patterns = set([x.strip() for x in f.readlines()])
        exclude_patterns = all_patterns - include_patterns
        return exclude_patterns


def _calculate_patterns_and_metrics(file_path: str, 
                                    is_decomposition_requested: bool,
                                    patterns_include: str=None,
                                    granularity: str='class') -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    config = Config.get_patterns_config()
    patterns_exclude = config["patterns_exclude"]
    if patterns_include is not None:
        patterns_exclude = get_unneeded_patterns(config['patterns'], args.patterns)
    patterns_info = [
        pattern_info
        for pattern_info in config["patterns"]
        if pattern_info["code"] not in patterns_exclude 
    ]

    metrics_info = [
        metric_info
        for metric_info in config["metrics"]
        if metric_info["code"] not in config["metrics_exclude"]
    ]

    ast = AST.build_from_javalang(build_ast(file_path))
    classes_ast = [
        ast.get_subtree(node)
        for node in ast.get_root().types
        if node.node_type == ASTNodeType.CLASS_DECLARATION
    ]

    ast_list = classes_ast
    if granularity == 'method':
        _class_ast = classes_ast[0]
        methods_ast = [
            _class_ast.get_subtree(node)
            for node in _class_ast.get_root().methods
        ]
        ast_list = methods_ast

    for _ast in ast_list:
        components = (
            decompose_java_class(_ast, "strong",  ignore_setters=True,  ignore_getters=True)
            if is_decomposition_requested
            else [_ast]
        )
        for index, component_ast in enumerate(components):
            if granularity == 'method':
                calculation_result = {
                    "filepath": file_path,
                    "_name": _ast.get_root().name,
                    "component_index": index   
                }
            else:
                calculation_result = {
                    "filepath": file_path,
                    "_name": _ast.get_root().name,
                    "component_index": index,
                }

            for pattern_info in patterns_info:
                try:
                    pattern = pattern_info["make"]()
                    if pattern_info['code'] == 'P28':
                        pattern_result = pattern.value(file_path)
                    else:
                        pattern_result = pattern.value(component_ast)
                    calculation_result[pattern_info["code"]] = len(pattern_result)
                    calculation_result["lines_" + pattern_info["code"]] = pattern_result
                except Exception as cause:
                    raise Exception(pattern_info['code'])# cause# FileProcessingError(file_path, pattern_info["name"], cause)

            for metric_info in metrics_info:
                try:
                    metric = metric_info["make"]()
                    metric_result = metric.value(component_ast)
                    calculation_result[metric_info["code"]] = metric_result
                except Exception as cause:
                    raise cause #FileProcessingError(file_path, metric_info["name"], cause)

            results.append(calculation_result)

    return results

def _create_dataset_writer(file, patterns_include=None):
    config = Config.get_patterns_config()
    
    patterns_exclude = config["patterns_exclude"]
    if patterns_include is not None:
        patterns_exclude = get_unneeded_patterns(config['patterns'], patterns_include)
    patterns_codes = [
        pattern["code"] for pattern in config["patterns"] if pattern["code"] not in patterns_exclude
    ]

    metrics_codes = [
        metric["code"] for metric in config["metrics"] if metric["code"] not in config["metrics_exclude"]
    ]

    fields = \
        patterns_codes + \
        metrics_codes + \
        ["lines_" + code for code in patterns_codes] + \
        ["filepath", "_name", "component_index"]
    return DictWriter(file, delimiter=";", quotechar='"', quoting=QUOTE_MINIMAL, fieldnames=fields)


def _parse_args():
    allowed_cores_qty = len(sched_getaffinity(0))
    system_cores_qty = cpu_count()

    parser = ArgumentParser(description="Creates dataset")
    parser.add_argument("--file", help="Path for file with a list of Java files.")

    parser.add_argument(
        "--jobs",
        "-j",
        type=int,
        default=min(allowed_cores_qty, system_cores_qty - 1),
        help="Number of processes to spawn. "
        "By default one less than number of cores. "
        "Be carefull to raise it above, machine may stop responding while creating dataset.",
    )

    parser.add_argument(
        "--timeout",
        "-t",
        type=float,
        default=3,
        help="Maximum time (in seconds) for single file proccessing. Default is 60 seconds. "
        "If 0, no timout is set.",
    )

    parser.add_argument(
        "--log",
        "-l",
        default="pattern_calculation.log",
        help="Path for log file. pattern_calculation.log is default.",
    )

    parser.add_argument(
        "--errors-log",
        "-el",
        default="calculation_errors.json",
        help="Path for errors log file. All errors grouped by patterns. calculation_errors.log is default.",
    )

    parser.add_argument(
        "--patterns",
        help='path to file with a list of patterns',
        required=False,
        default=None)

    parser.add_argument(
        '--granularity',
        help='Granularity level: class or method',
        required=False,
        default='class')

    args = parser.parse_args()

    if args.jobs >= system_cores_qty:
        print(
            f"WARNING: You have ordered to spawn {args.jobs} jobs, "
            f"while system has only {system_cores_qty} cores. "
            "Machine may badly respond, while calculating dataset.",
            file=stderr,
        )

    if args.jobs > allowed_cores_qty:
        print(
            f"WARNING: You have ordered to spawn {args.jobs} jobs, "
            f"while process only allowed to occupy {allowed_cores_qty} cores."
            "You may have a slowdown due to large number of processes.",
            file=stderr,
        )

    if args.timeout == 0:
        args.timeout = None

    basicConfig(filename=args.log, filemode="w", level=INFO)

    default_dataset_directory = Path(".", "target", "04").absolute()
    dataset_directory = getenv("TARGET_FOLDER", default=default_dataset_directory)
    makedirs(dataset_directory, exist_ok=True)
    args.csv_file = Path(dataset_directory, "04-find-patterns.csv")

    is_decomposition_requested = getenv("LCOM_DECOMPOSITION", "True")
    if is_decomposition_requested in {"True", "1"}:
        args.is_decomposition_requested = True
    elif is_decomposition_requested in {"False", "0"}:
        args.is_decomposition_requested = False
    else:
        print(
            f"WARNING: value of 'LCOM_DECOMPOSITION' environment variable {is_decomposition_requested} "
            "is not recognized. Avaliable options are 'True', 'False', '1', '0'."
            "Decomposition is applied by default.",
            file=stderr,
        )
        args.is_decomposition_requested = True

    return args


if __name__ == "__main__":
    args = _parse_args()

    errors: List[FileProcessingError] = []
    timeout_errors_qty = 0
    parsing_errors_qty = 0

    calculate_patterns_and_metrics = partial(
        _calculate_patterns_and_metrics, is_decomposition_requested=args.is_decomposition_requested,
        patterns_include=args.patterns, granularity=args.granularity
    )
    with open(args.file) as input, open(args.csv_file, "w") as output, ProcessPool(args.jobs) as executor:
        dataset_writer = _create_dataset_writer(output, patterns_include=args.patterns)
        dataset_writer.writeheader()

        filenames = [filename.rstrip() for filename in input.readlines()]
        future = executor.map(calculate_patterns_and_metrics, filenames, timeout=args.timeout,)
        dataset_features = future.result()

        for filename in tqdm(filenames):
            try:
                single_file_features = next(dataset_features)
                dataset_writer.writerows(single_file_features)
            except TimeoutError:
                warning(f"Processing {filename} is aborted due to timeout in {args.timeout} seconds.")
                timeout_errors_qty += 1
            except Exception as e:
                warning(e)
                parsing_errors_qty += 1
                if isinstance(e, FileProcessingError):
                    errors.append(e)

    if timeout_errors_qty or parsing_errors_qty:
        print(
            f"WARNING: There was {timeout_errors_qty} timeouts and "
            f"{parsing_errors_qty} errors during file processing.\n"
            f"Check {args.log} for detailed information.",
            file=stderr,
        )

    if len(errors) > 0:
        errors_by_pattern = defaultdict(dict)
        for error in errors:
            errors_by_pattern[error.pattern_name][error.filepath] = str(error.cause)

        with open(args.errors_log, "w") as errors_log:
            json.dump(errors_by_pattern, errors_log)

        print(
            f"WARNING: All errors grouped by pattern/metric name ind written to {args.errors_log}",
            file=stderr,
        )
