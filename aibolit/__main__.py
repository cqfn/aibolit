#!/usr/bin/env python
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

"""The main entry point. Invoke as `aibolit' or `python -m aibolit'.
"""

import argparse
import concurrent.futures
import json
import multiprocessing
import operator
import os
import pickle
import sys
import time
import traceback
from collections import defaultdict, OrderedDict
from os import scandir
from pathlib import Path
from sys import stdout
from typing import List, Any, Dict, Tuple

import javalang
from javalang.parser import JavaSyntaxError
import numpy as np  # type: ignore
import requests  # type: ignore[import-untyped]
from lxml import etree  # type: ignore
from packaging.version import parse as parse_version

from aibolit import __version__
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_decomposition import decompose_java_class
from aibolit.config import Config
from aibolit.metrics.ncss.ncss import NCSSMetric
from aibolit.ml_pipeline.ml_pipeline import train_process, collect_dataset
from aibolit.utils.ast_builder import build_ast

dir_path = os.path.dirname(os.path.realpath(__file__))


def list_dir(path, files):
    dir_list = []
    for entry in scandir(path):
        if entry.is_dir():
            dir_list.append(entry.path)
            dir_list.extend(list_dir(entry.path, files))
        elif entry.is_file() \
                and entry.path.endswith('.java') \
                and entry.name != 'package-info.java':
            files.append(entry.path)
    return dir_list


def run_parse_args(commands_dict):
    parser = argparse.ArgumentParser(
        description='Find the pattern which has the largest impact on readability',
        usage='''aibolit <command> [<args>]

        You can run 1 command:
        train          Train model
        check          Recommend pattern
        recommend      Recommend pattern. The same as recommend, just another acronym''')

    parser.add_argument('command', help='Subcommand to run')
    parser.add_argument(
        '--version', action='version',
        version=f'%(prog)s {__version__}'
    )
    # parse_args defaults to [1:] for args, but you need to
    # exclude the rest of the args too, or validation will fail
    args = parser.parse_args(sys.argv[1:2])
    if args.command not in commands_dict:
        parser.print_help()
        exit(1)

    return commands_dict[args.command]()


def train():
    parser = argparse.ArgumentParser(
        description='Collect dataset and train model'
    )
    parser.add_argument(
        '--java_folder',
        help='full path to directory',
        default=False,
        required=False
    )
    parser.add_argument(
        '--max_classes',
        type=lambda v: sys.maxsize if v == '' else int(v),
        required=False,
        default=None
    )
    parser.add_argument(
        '--skip_collect_dataset',
        required=False,
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--dataset_file',
        required=False,
        default=False
    )
    parser.add_argument(
        "--target-metric",
        choices=["rfc", "fanout", "diameter", "cognitive"],
        default="cognitive",
        help="Select target metric. Available metrics: rfc, fanout, diameter, cognitive. "
             "Default is cognitive."
    )
    args = parser.parse_args(sys.argv[2:])
    if not args.skip_collect_dataset:
        collect_dataset(args)

    metric_name_to_code = {
        "rfc": "M9",
        "fanout": "M10",
        "diameter": "M6",
        "cognitive": "M4",
    }
    train_process(metric_name_to_code[args.target_metric])


def __count_value(value_dict, input_params, code_lines_dict, java_file: str, is_metric=False):
    """
    Count value for input dict

    :param value_dict: Pattern item or Metric item from CONFIG
    :param input_params: list with calculated patterns/metrics
    :param code_lines_dict: list with found code lines of patterns/metrics
    :param java_file: full path for java file
    :is_metric: is item metric?
    :return: None, it has side-effect
    """
    acronym = value_dict['code']
    try:
        ast = AST.build_from_javalang(build_ast(java_file))
        val = value_dict['make']().value(ast)
        if not is_metric:
            input_params[acronym] = len(val)
            code_lines_dict['lines_' + acronym] = val
        else:
            input_params[acronym] = val
    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        raise Exception(f"Can't count {acronym} metric: {str(type(exc_value))}")


def flatten(lst):
    return [item for sublist in lst for item in sublist]


def add_pattern_if_ignored(
        dct: Dict[str, Any],
        pattern_item: Dict[Any, Any],
        results_list: List[Any]) -> None:
    """ If pattern code is not ignored, add it to the result list

    :param dct: dict, where key is pattern, value is list of lines range to ignore
    :param pattern_item: pattern dict which was get after `inference` function
    :param results_list: result list to add

    """
    ignored_lines = dct.get(pattern_item['pattern_code'])
    if ignored_lines:
        for place in ignored_lines:
            # get lines range of ignored code
            start_line_to_ignore = place[0]
            end_line_to_ignore = place[1]
            new_code_lines = []
            for line in pattern_item['code_lines']:
                if start_line_to_ignore <= line <= end_line_to_ignore:
                    continue
                else:
                    new_code_lines.append(line)
            pattern_item['code_lines'] = new_code_lines
            if len(pattern_item['code_lines']) > 0:
                results_list.append(pattern_item)
    else:
        results_list.append(pattern_item)


def find_annotation_by_node_type(
        tree: javalang.tree.CompilationUnit,
        node_type) -> Dict[Any, Any]:
    """Search nodes with annotations.

    :param tree: javalang.tree
    :param node_type: Node type of javalang.tree
    :return
    dict with annotations, where key is node, value is list of string annotations;
    """
    annonations = defaultdict(list)
    for _, node in tree.filter(node_type):
        if node.annotations:
            for a in node.annotations:
                if hasattr(a.element, 'value'):
                    if 'aibolit' in a.element.value:
                        annonations[node].append(
                            a.element.value.split('.')[1].rstrip('\"')
                        )
                elif hasattr(a.element, 'values'):
                    for j in a.element.values:
                        if 'aibolit' in j.value:
                            annonations[node].append(
                                j.value.split('.')[1].rstrip('\"')
                            )
    return annonations


def find_start_and_end_lines(node) -> Tuple[int, int]:  # noqa: C901
    max_line = node.position.line

    def check_max_position(node):
        nonlocal max_line
        if hasattr(node, '_position'):
            if node.position.line > max_line:
                max_line = node.position.line

    def traverse(node):
        check_max_position(node)

        if hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, list) and (len(child) > 0):
                    for item in child:
                        if isinstance(item, list):
                            for i in item:
                                traverse(i)
                        else:
                            traverse(item)
                else:
                    if hasattr(child, 'children'):
                        infants = child.children
                        for infant in infants:
                            if isinstance(infant, list):
                                for j in infant:
                                    traverse(j)
                            else:
                                traverse(infant)
                    else:
                        check_max_position(child)

    traverse(node)
    return node.position.line, max_line


def calculate_patterns_and_metrics_with_decomposition(
        file_path: str,
        args):
    error_exc = None
    patterns_to_suppress = args.suppress
    results_for_components = []

    try:
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
                result_for_component: Dict[Any, Any] = {}
                code_lines_dict: Dict[Any, Any] = OrderedDict()
                input_params = OrderedDict()  # type: ignore

                for pattern_info in patterns_info:
                    if pattern_info['code'] in config['patterns_exclude']:
                        continue
                    if pattern_info['code'] in patterns_to_suppress:
                        input_params[pattern_info["code"]] = 0
                        code_lines_dict["lines_" + pattern_info["code"]] = []
                    else:
                        pattern = pattern_info["make"]()
                        pattern_result = pattern.value(component_ast)
                        input_params[pattern_info["code"]] = len(pattern_result)
                        code_lines_dict["lines_" + pattern_info["code"]] = pattern_result

                for metric_info in metrics_info:
                    metric = metric_info["make"]()
                    metric_result = metric.value(component_ast)
                    input_params[metric_info["code"]] = metric_result

                result_for_component['code_lines_dict'] = code_lines_dict
                result_for_component['input_params'] = input_params
                result_for_component['index'] = index
                results_for_components.append(result_for_component)
    except Exception as ex:
        error_exc = ex

    return results_for_components, error_exc


def calculate_patterns_and_metrics(file, args):
    code_lines_dict = input_params = {}  # type: ignore
    error_exc = None
    patterns_to_suppress = args.suppress
    try:
        config = Config.get_patterns_config()
        for pattern in config['patterns']:
            if pattern['code'] in config['patterns_exclude']:
                continue
            if pattern['code'] in patterns_to_suppress:
                input_params[pattern['code']] = 0
            else:
                __count_value(pattern, input_params, code_lines_dict, file)

        for metric in config['metrics']:
            if metric['code'] in config['metrics_exclude']:
                continue
            __count_value(metric, input_params, code_lines_dict, file, is_metric=True)
    except Exception as ex:
        error_exc = ex
        input_params = []  # type: ignore

    return input_params, code_lines_dict, error_exc


def inference(
        input_params: Dict[Any, Any],
        code_lines_dict,
        args):
    """
    Find a pattern which has the largest impact on target

    :param input_params: list if calculated patterns/metrics
    :param code_lines_dict: list with found code lines of patterns/metrics
    :param file: filename

    :return: list of results with code_lies for each pattern and its name
    """
    model_path = args.model
    do_full_report = args.full
    results = []
    if input_params:
        if not model_path:
            model_path = Config.folder_model_data()
        with open(model_path, 'rb') as fid:
            model = pickle.load(fid)
        sorted_result, importances = model.predict(input_params)
        patterns_list = model.features_conf['features_order']
        for iter, (key, val) in enumerate(sorted_result.items()):
            if key in patterns_list:
                pattern_code = key
                code_lines = code_lines_dict.get('lines_' + key)
                importance = importances[iter] * input_params[pattern_code]

                # We show only patterns with positive importance
                if code_lines and importance > 0:
                    if code_lines:
                        pattern_name = \
                            [x['name'] for x in Config.get_patterns_config()['patterns']
                             if x['code'] == pattern_code][0]
                        results.append(
                            {'code_lines': code_lines,
                             'pattern_code': pattern_code,
                             'pattern_name': pattern_name,
                             'importance': importance
                             })
                    if not do_full_report:
                        break
    else:
        return results

    return results


def create_results(
        input_params: Dict[Any, Any],
        code_lines_dict: Dict[Any, Any],
        args: argparse.Namespace,
        classes_with_patterns_ignored: List[Any],
        patterns_ignored: Dict[Any, Any]):

    results_list = inference(input_params, code_lines_dict, args)
    new_results: List[Any] = []
    for pattern_item in results_list:
        # check if the whole class is suppressed
        if pattern_item['pattern_code'] not in classes_with_patterns_ignored:
            # then check if patterns are ignored in fields or functions
            add_pattern_if_ignored(patterns_ignored, pattern_item, new_results)
            # add_pattern_if_ignored(patterns_for_fields_ignored, pattern_item, new_results)
        else:
            continue

    return new_results


def _extract_patterns_ignored(tree):
    """Extract patterns that should be ignored from annotations."""
    classes_with_annonations = find_annotation_by_node_type(
        tree, javalang.tree.ClassDeclaration)
    functions_with_annotations = find_annotation_by_node_type(
        tree, javalang.tree.MethodDeclaration)
    fields_with_annotations = find_annotation_by_node_type(
        tree, javalang.tree.FieldDeclaration)
    classes_with_patterns_ignored = flatten(
        [pattern_code for node, pattern_code in classes_with_annonations.items()])
    patterns_ignored = defaultdict(list)

    for node, patterns_list in functions_with_annotations.items():
        start_pos, end_pos = find_start_and_end_lines(node)
        for p in patterns_list:
            patterns_ignored[p].append([start_pos, end_pos])

    for node, patterns_list in fields_with_annotations.items():
        for p in patterns_list:
            patterns_ignored[p].append([node.position.line,
                                       node.position.line])

    return classes_with_patterns_ignored, patterns_ignored


def _process_components(components, args, classes_with_patterns_ignored, patterns_ignored):
    """Process components to create results."""
    results_list = []
    for lcom_component in components:
        code_lines_dict = lcom_component.get('code_lines_dict')
        input_params = lcom_component.get('input_params')
        ranked_results = create_results(
            input_params,
            code_lines_dict,
            args,
            classes_with_patterns_ignored,
            patterns_ignored
        )
        if ranked_results:
            results_list.append(ranked_results)
    return results_list


def run_recommend_for_file(file: str, args):  # flake8: noqa
    """
    Calculate patterns and metrics, pass values to model and suggest pattern to change
    :param file: file to analyze
    :param args: different command line arguments
    :return: dict with code lines, filename and pattern name
    """
    java_file = str(Path(os.getcwd(), file))
    ncss = 0
    try:
        tree = build_ast(file)
        classes_with_patterns_ignored, patterns_ignored = _extract_patterns_ignored(tree)

        components, error_exception = calculate_patterns_and_metrics_with_decomposition(
            java_file, args)

        if not components:
            results_list = []  # type: ignore
            error_exception = 'Empty java file; ncss = 0'
        else:
            results_list = _process_components(
                components, args, classes_with_patterns_ignored, patterns_ignored)

        ncss = NCSSMetric().value(AST.build_from_javalang(build_ast(file)))
    except Exception as e:
        error_exception = e
        ncss = 0
        results_list = []

    return {
        'filename': file,
        'results': results_list,
        'exception': error_exception,
        'ncss': ncss,
    }


def _process_pattern(patterns_tag, pattern, i, patterns_number):
    """Process a single pattern and add it to the XML."""
    pattern_item = etree.SubElement(patterns_tag, 'pattern')
    pattern_name_str = pattern.get('pattern_name')
    details = etree.SubElement(pattern_item, 'details')
    details.text = pattern_name_str or ''
    pattern_item.attrib['code'] = pattern.get('pattern_code')
    code_lines_items = pattern.get('code_lines')
    pattern_score = pattern.get('importance')
    pattern_score_tag = etree.SubElement(pattern_item, 'score')
    pattern_score_tag.text = f'{pattern_score:.2f}' or ''
    pattern_score_tag = etree.SubElement(pattern_item, 'order')
    pattern_score_tag.text = f'{i}/{patterns_number}'

    if code_lines_items:
        code_lines_lst_tree_node = etree.SubElement(pattern_item, 'lines')
        for code_line in code_lines_items:
            code_line_elem = etree.SubElement(code_lines_lst_tree_node, 'number')
            code_line_elem.text = str(code_line)

    return pattern_score


def _process_file_result(file, result_for_file):
    """Process a single file result and add it to the XML."""
    filename = result_for_file.get('filename')
    name = etree.SubElement(file, 'path')
    output_string_tag = etree.SubElement(file, 'summary')
    name.text = filename
    results_item = result_for_file.get('results')
    ex = result_for_file.get('exception')
    errors_string = str(result_for_file.get('exception')) or type(ex).__name__

    if not results_item and not errors_string:
        output_string = 'Your code is perfect in aibolit\'s opinion'
        output_string_tag.text = output_string
        return None
    elif not results_item and errors_string:
        output_string = f'Error when calculating patterns: {str(errors_string)}'
        output_string_tag.text = output_string
        return None
    else:
        output_string = 'Some issues found'
        output_string_tag.text = output_string
        importances_sum_tag = etree.SubElement(file, 'score')
        patterns_tag = etree.SubElement(file, 'patterns')
        patterns_number = len(result_for_file['results'])
        importance_for_class = []

        for i, pattern in enumerate(result_for_file['results'], start=1):
            if pattern.get('pattern_code'):
                pattern_score = _process_pattern(patterns_tag, pattern, i, patterns_number)
                importance_for_class.append(pattern_score)

        score_for_class = sum(importance_for_class)
        importances_sum_tag.text = str(score_for_class)
        return score_for_class


def _create_xml_header(top, results, cmd, exit_code):
    """Create XML header with metadata."""
    header_tag = etree.SubElement(top, 'header')
    importances_for_all_classes_tag = etree.SubElement(header_tag, 'score')
    datetime_tag = etree.SubElement(header_tag, 'datetime')
    datetime_tag.addprevious(etree.Comment('datetime in ms'))
    datetime_tag.text = str(int(round(time.time() * 1000)))
    version_tag = etree.SubElement(header_tag, 'version')
    version_tag.text = str(__version__)
    files_number_tag = etree.SubElement(header_tag, 'files')
    files_number_tag.addprevious(etree.Comment('Files with found patterns'))
    files_number_tag.text = str(len(
        [x for x in results
         if (not x.get('exception') and x.get('results'))]
    ))
    patterns_number_tag = etree.SubElement(header_tag, 'patterns')
    ncss_tag = etree.SubElement(header_tag, 'ncss')
    ncss_tag.text = str(sum([x['ncss'] for x in results]))
    cmd_tag = etree.SubElement(header_tag, 'cmd')
    cmd_tag.text = ' '.join(cmd)
    cmd_tag = etree.SubElement(header_tag, 'exit_code')
    cmd_tag.text = str(exit_code)
    return importances_for_all_classes_tag, patterns_number_tag


def create_xml_tree(results, full_report, cmd, exit_code):
    """
    Creates xml from output of `check` function
    :param results: output of `check` function
    :return: xml string
    """
    importances_for_all_classes = []
    top = etree.Element('report')
    importances_tag, patterns_number_tag = _create_xml_header(top, results, cmd, exit_code)

    total_patterns = 0
    files = etree.SubElement(top, 'files')
    if not full_report:
        files.addprevious(etree.Comment(
            'Show pattern with the largest contribution to Cognitive Complexity'))
    else:
        files.addprevious(etree.Comment('Show all patterns'))
    for result_for_file in results:
        file = etree.SubElement(files, 'file')
        score_for_file = _process_file_result(file, result_for_file)
        if score_for_file is not None:
            total_patterns += len(result_for_file['results'])
            importances_for_all_classes.append(score_for_file)

    patterns_number_tag.text = str(total_patterns)
    if importances_for_all_classes:
        importances_tag.text = str(np.mean(importances_for_all_classes))

    return top


def get_exit_code(results):
    """
    Analyzed recommendation results and generate exit_code for pipeline
    """

    files_analyzed = len(results)
    errors_number = 0
    perfect_code_number = 0
    errors_strings = []
    for result_for_file in results:
        results = result_for_file.get('results')
        ex = result_for_file.get('exception')
        if not results and not ex:
            perfect_code_number += 1
        elif not results and ex:
            if not isinstance(ex, JavaSyntaxError):
                errors_strings.append(ex)
                errors_number += 1
            else:
                # ignore JavaSyntaxError, it is expected error
                perfect_code_number += 1

    if len(errors_strings) == files_analyzed:
        # we have errors everywhere
        exit_code = 2
    elif perfect_code_number == files_analyzed:
        # everything is good
        exit_code = 0
    else:
        # we have some recommendation
        exit_code = 1

    return exit_code


def create_text(results, full_report, is_long=False):
    importances_for_all_classes = []
    buffer = []
    total_patterns = 0
    if not full_report:
        buffer.append('Show pattern with the largest contribution to Cognitive Complexity')
    else:
        buffer.append('Show all patterns')
    for result_for_file in results:
        filename = result_for_file.get('filename')
        results_item = result_for_file.get('results')
        ex = result_for_file.get('exception')
        if not results_item and not ex:
            # Do nothing, patterns were not found
            pass
        if not results_item and ex:
            output_string = (f'{filename}: error when calculating patterns: '
                             f'{str(ex) or type(ex).__name__}')
            buffer.append(output_string)
        elif results_item and not ex:
            # get unique patterns score
            pattern_number = 0
            cur_pattern_name = ''
            for pattern_item in result_for_file['results']:
                pattern_score = pattern_item.get('importance')
                code = pattern_item.get('pattern_code')
                if code:
                    pattern_name_str = pattern_item.get('pattern_name')
                    if cur_pattern_name != pattern_name_str:
                        pattern_number += 1
                        cur_pattern_name = pattern_name_str
                    buffer.append(f'{filename}[{pattern_item.get("code_line")}]: '
                                  f'{pattern_name_str} ({code}: {pattern_score:.2f})')

            total_patterns += pattern_number
    if importances_for_all_classes:
        show_summary(buffer, importances_for_all_classes, is_long, results, total_patterns)

    return buffer


def show_summary(buffer, importances_for_all_classes, is_long, results, total_patterns):
    files_number = len(
        [x for x in results
         if (not x.get('errors_string') and x.get('results'))
         ])
    ncss = sum(
        [x['ncss'] for x in results
         if (not x.get('errors_string') and x.get('results'))])
    if not is_long:
        buffer.append(f'Total score: {np.mean(importances_for_all_classes):.2f}, '
                      f'files seen: {files_number}, patterns found: {total_patterns}, '
                      f'ncss: {ncss}')
    else:
        buffer.append(f'Total score: {np.mean(importances_for_all_classes):.2f}, '
                      f'files seen: {files_number}, ncss {ncss}')
        url = 'https://github.com/cqfn/aibolit/blob/master/PATTERNS.md'
        buffer.append(f'You can find all information about patterns here: {url}')


def print_total_score_for_file(
        buffer: List[str],
        filename: str,
        importances_for_all_classes: List[int],
        result_for_file):
    patterns_scores = {}
    for x in result_for_file['results']:
        patterns_scores[x['pattern_name']] = x['importance']
    importances_for_class = sum(patterns_scores.values())
    importances_for_all_classes.append(importances_for_class)
    buffer.append(f'{filename} score: {importances_for_class}')
    return patterns_scores


def check():
    """Run check pipeline."""

    parser = argparse.ArgumentParser(
        description='Get recommendations for Java code',
        usage='aibolit check < --folder | --filenames > [--model] '
              '[--threshold] [--full] [--format]')

    group_exclusive = parser.add_mutually_exclusive_group(required=True)

    group_exclusive.add_argument(
        '--folder',
        help='path to Java files',
        default=False
    )
    group_exclusive.add_argument(
        '--filenames',
        help='list of Java files',
        nargs="*",
        default=False
    )
    parser.add_argument(
        '--model',
        help='''file where pretrained model is located, the default path is located
        in site-packages and is installed with aibolit automatically''',
        default=False
    )
    parser.add_argument(
        '--full',
        help='show all recommendations instead of the best one',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--format',
        default='compact',
        help='compact (by default), long or xml. Usage: --format=xml'
    )

    parser.add_argument(
        '--suppress',
        default=[],
        help='Suppress certain patterns (comma separated value)'
    )
    parser.add_argument(
        '--exclude',
        action='append',
        nargs='+',
        default=[],
        help='Glob patterns to ignore. '
    )
    args = parser.parse_args(sys.argv[2:])

    if args.suppress:
        args.suppress = args.suppress.strip().split(',')

    files_to_exclude = handle_exclude_command_line(args)

    files = []
    if args.filenames:
        files = [str(Path(x).absolute()) for x in args.filenames if x not in files_to_exclude]
    elif args.folder:
        all_files = []
        list_dir(args.folder, all_files)
        files = [str(Path(x).absolute()) for x in all_files if str(x) not in files_to_exclude]

    results = list(run_thread(files, args))
    exit_code = get_exit_code(results)

    if args.format:
        if args.format == 'xml':
            root = create_xml_tree(results, args.full, sys.argv, exit_code)
            tree = root.getroottree()
            tree.write(stdout.buffer, pretty_print=True)
        else:
            if args.format in ['compact', 'short']:
                new_results = format_converter_for_pattern(results)
            elif args.format == 'long':
                new_results = format_converter_for_pattern(results, 'code_line')
            else:
                raise Exception('Unknown format')

            text = create_text(new_results, args.full, True)

            if args.format == 'short':
                print(text[-1])
            else:
                print('\n'.join(text))

    return exit_code


def handle_exclude_command_line(args: Any) -> List[str]:
    files_to_exclude: List[str] = []
    full_path_to_exclude = args.folder
    glob_patterns = args.exclude
    for glob_p in glob_patterns:
        pattern = glob_p[0]
        files_to_exclude.extend([str(x.absolute())
                                for x in Path(full_path_to_exclude).glob(pattern)])
    print("ignore:", files_to_exclude)
    return files_to_exclude


def format_converter_for_pattern(results, sorted_by=None):
    """
    Reformat data where data are sorted by patterns importance
    (it is already sorted in the input).
    Then lines are sorted in ascending order.
    """
    total_patterns_list = []
    for file in results:
        components = file.get('results')
        all_results = {}
        if components:
            for i, component in enumerate(components):
                new_items = flatten([
                    [{'pattern_code': x['pattern_code'],
                      'pattern_name': x['pattern_name'],
                      'code_line': line,
                      'importance': x['importance']
                      } for line in sorted(x['code_lines'])] for x in component
                ])
                if not sorted_by:
                    all_results[i] = sorted(
                        new_items,
                        key=lambda e: (-e['importance'], e['pattern_code'], e['code_line'])
                    )
                else:
                    all_results[i] = new_items

        if not sorted_by:
            # iterate over all components, get 1st importance for 1st component,
            # then 1st importance for 2nd component, etc.
            while len(all_results) > 0:
                for idx in list(all_results):
                    componet_res = all_results[idx]
                    top_pattern = componet_res.pop()
                    total_patterns_list.append(top_pattern)
                    if not componet_res:
                        del all_results[idx]
        else:
            for _, val in all_results.items():
                total_patterns_list.extend(val)
            total_patterns_list = sorted(total_patterns_list,
                                         key=operator.itemgetter(sorted_by, 'pattern_code'))

        file['results'] = total_patterns_list

    return results


def version():
    """
    Parses arguments and shows current version of program.
    """

    parser = argparse.ArgumentParser(
        description='Show version')
    parser.add_argument(
        '--version',
    )
    print(f'%(prog)s {__version__}')


def run_thread(files, args):
    """
    Parallel patterns/metrics calculation
    :param files: list of java files to analyze

    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        future_results = [executor.submit(run_recommend_for_file, file, args) for file in files]
        concurrent.futures.wait(future_results)
        for future in future_results:
            yield future.result()


def get_versions(pkg_name):
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    releases = json.loads(requests.get(url, timeout=15).content)['releases']
    return sorted(releases, key=parse_version, reverse=True)


def main():
    try:
        max_available_version = get_versions('aibolit')[0]
        if max_available_version != __version__:
            print(f'Version {max_available_version} is available, but you are using {__version__}')
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,
            requests.exceptions.ReadTimeout):
        print('Can\'t check aibolit version. Network is not available')
    try:
        commands = {
            'train': train,
            'check': check,
            'recommend': check,
            'version': version,
        }
        exit_code = run_parse_args(commands)
    except Exception:
        traceback.print_exc()
        sys.exit(2)
    else:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
