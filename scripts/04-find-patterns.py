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
from concurrent.futures import TimeoutError
from csv import DictWriter, QUOTE_MINIMAL
from os import cpu_count, getenv, makedirs, sched_getaffinity
from pathlib import Path
from sys import stderr
from typing import Any, Dict, List

from pebble import ProcessPool
from tqdm import tqdm

from aibolit.config import Config
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.utils.ast_builder import build_ast


def _calculate_patterns_and_metrics(file_path: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    config = Config.get_patterns_config()
    patterns_info = [
        pattern_info
        for pattern_info in config["patterns"]
        if pattern_info["code"] not in config["patterns_exclude"]
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

    for class_ast in classes_ast:
        for index, component_ast in enumerate(decompose_java_class(class_ast, "strong")):
            calculation_result = {"filepath": file_path, "component_index": index}

            for pattern_info in patterns_info:
                pattern = pattern_info["make"]()
                pattern_result = pattern.value(component_ast)
                calculation_result[pattern_info["code"]] = len(pattern_result)
                calculation_result["lines_" + pattern_info["code"]] = pattern_result

            for metric_info in metrics_info:
                metric = metric_info["make"]()
                metric_result = metric.value(component_ast)
                calculation_result[metric_info["code"]] = metric_result

            results.append(calculation_result)

    return results


def _create_dataset_writer(file):
    config = Config.get_patterns_config()

    patterns_codes = [
        pattern["code"] for pattern in config["patterns"] if pattern["code"] not in config["patterns_exclude"]
    ]

    metrics_codes = [
        metric["code"] for metric in config["metrics"] if metric["code"] not in config["metrics_exclude"]
    ]

    fields = \
        patterns_codes + \
        metrics_codes + \
        ["lines_" + code for code in patterns_codes] + \
        ["filepath", "component_index"]

    return DictWriter(file, delimiter=";", quotechar='"', quoting=QUOTE_MINIMAL, fieldnames=fields)


if __name__ == "__main__":
    allowed_cores_qty = len(sched_getaffinity(0))
    system_cores_qty = cpu_count()

    parser = ArgumentParser(description="Creates dataset")
    parser.add_argument("file", help="Path for file with a list of Java files.")

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
        default=60,
        help="Maximum time (in seconds) for single file proccessing. Default is 60 seconds. "
        "If 0, no timout is set.",
    )

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

    default_dataset_directory = Path(".", "target", "04").absolute()
    dataset_directory = getenv("TARGET_FOLDER", default=default_dataset_directory)
    makedirs(dataset_directory, exist_ok=True)
    csv_file = Path(dataset_directory, "04-find-patterns.csv")

    with open(args.file) as input, open(csv_file, "w") as output, ProcessPool(args.jobs) as executor:
        dataset_writer = _create_dataset_writer(output)
        dataset_writer.writeheader()

        filenames = [filename.rstrip() for filename in input.readlines()]
        future = executor.map(_calculate_patterns_and_metrics, filenames, timeout=args.timeout)
        dataset_features = future.result()

        for filename in tqdm(filenames):
            try:
                single_file_features = next(dataset_features)
                dataset_writer.writerows(single_file_features)
            except TimeoutError:
                print(
                    f"Processing {filename} is aborted due to timeout in {args.timeout} seconds.", file=stderr
                )
            except Exception as e:
                print(f"Processing {filename} has end up with error {e}.", file=stderr)
