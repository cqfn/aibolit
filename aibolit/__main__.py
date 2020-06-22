#!/usr/bin/env python
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
from os import scandir
from pathlib import Path
from sys import stdout
from typing import List
import numpy as np  # type: ignore
import requests
from lxml import etree  # type: ignore
from pkg_resources import parse_version

from aibolit import __version__
from aibolit.config import Config
from aibolit.ml_pipeline.ml_pipeline import train_process, collect_dataset
from aibolit.model.model import TwoFoldRankingModel, Dataset  # type: ignore  # noqa: F401

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


def predict(input_params, model, args):
    features_order = model.features_conf['features_order']
    # add ncss to last column. We will normalize all patterns by that value
    # deepcode ignore ExpectsIntDislikesStr: false-positive recommendation of deepcode
    input = [input_params[i] for i in features_order] + [input_params['M2']]
    th = float(args.threshold) or 1.0
    preds, importances = model.informative(input, th=th)

    return {features_order[int(x)]: int(x) for x in preds}, list(importances)


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
        version='%(prog)s {version}'.format(version=__version__)
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
    args = parser.parse_args(sys.argv[2:])
    if not args.skip_collect_dataset:
        collect_dataset(args)
    train_process()


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
        val = value_dict['make']().value(java_file)
        if not is_metric:
            input_params[acronym] = len(val)
            code_lines_dict['lines_' + acronym] = val
        else:
            input_params[acronym] = val
    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        raise Exception("Can't count {} metric: {}".format(
            acronym,
            str(exc_value))
        )


def calculate_patterns_and_metrics(file, args):
    code_lines_dict = input_params = {}  # type: ignore
    error_string = None
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
        error_string = str(ex)
        input_params = []  # type: ignore

    return input_params, code_lines_dict, error_string


def inference(
        input_params: List[int],
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
        sorted_result, importances = predict(input_params, model, args)
        patterns_list = model.features_conf['patterns_only']
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


def run_recommend_for_file(file: str, args):
    """
    Calculate patterns and metrics, pass values to model and suggest pattern to change
    :param file: file to analyze
    :param args: different command line arguments
    :return: dict with code lines, filename and pattern name
    """
    java_file = str(Path(os.getcwd(), file))
    input_params, code_lines_dict, error_string = calculate_patterns_and_metrics(java_file, args)
    results_list = inference(input_params, code_lines_dict, args)

    return {
        'filename': file,
        'results': results_list,
        'error_string': error_string
    }


def create_xml_tree(results, full_report, cmd, exit_code):
    """
    Creates xml from output of `check` function
    :param results: output of `check` function
    :return: xml string
    """
    importances_for_all_classes = []
    top = etree.Element('report')
    header_tag = etree.SubElement(top, 'header')
    importances_for_all_classes_tag = etree.SubElement(header_tag, 'score')
    datetime_tag = etree.SubElement(header_tag, 'datetime')
    datetime_tag.addprevious(etree.Comment('datetime in ms'))
    datetime_tag.text = str(int(round(time.time() * 1000)))
    version_tag = etree.SubElement(header_tag, 'version')
    version_tag.text = str(__version__)
    cmd_tag = etree.SubElement(header_tag, 'cmd')
    cmd_tag.text = ' '.join(cmd)
    cmd_tag = etree.SubElement(header_tag, 'exit_code')
    cmd_tag.text = str(exit_code)

    files = etree.SubElement(top, 'files')
    if not full_report:
        files.addprevious(etree.Comment('Show pattern with the largest contribution to Cognitive Complexity'))
    else:
        files.addprevious(etree.Comment('Show all patterns'))
    for result_for_file in results:
        file = etree.SubElement(files, 'file')
        filename = result_for_file.get('filename')
        name = etree.SubElement(file, 'path')
        output_string_tag = etree.SubElement(file, 'summary')
        name.text = filename
        results = result_for_file.get('results')
        errors_string = result_for_file.get('error_string')
        if not results and not errors_string:
            output_string = 'Your code is perfect in aibolit\'s opinion'
            output_string_tag.text = output_string
        elif not results and errors_string:
            output_string = 'Error when calculating patterns: {}'.format(str(errors_string))
            output_string_tag.text = output_string
        else:
            output_string = 'Some issues found'
            output_string_tag.text = output_string
            importances_sum_tag = etree.SubElement(file, 'score')
            patterns_tag = etree.SubElement(file, 'patterns')
            patterns_number = len(result_for_file['results'])
            importance_for_class = []
            for i, pattern in enumerate(result_for_file['results'], start=1):
                if pattern.get('pattern_code'):
                    pattern_item = etree.SubElement(patterns_tag, 'pattern')
                    pattern_name_str = pattern.get('pattern_name')
                    details = etree.SubElement(pattern_item, 'details')
                    details.text = pattern_name_str or ''
                    pattern_item.attrib['code'] = pattern.get('pattern_code')
                    code_lines_items = pattern.get('code_lines')
                    pattern_score = pattern.get('importance')
                    pattern_score_tag = etree.SubElement(pattern_item, 'score')
                    pattern_score_tag.text = '{:.2f}'.format(pattern_score) or ''
                    pattern_score_tag = etree.SubElement(pattern_item, 'order')
                    pattern_score_tag.text = '{}/{}'.format(i, patterns_number)
                    importance_for_class.append(pattern_score)
                    if code_lines_items:
                        code_lines_lst_tree_node = etree.SubElement(pattern_item, 'lines')
                        for code_line in code_lines_items:
                            code_line_elem = etree.SubElement(code_lines_lst_tree_node, 'number')
                            code_line_elem.text = str(code_line)
            score_for_class = sum(importance_for_class)
            importances_sum_tag.text = str(score_for_class)
            importances_for_all_classes.append(score_for_class)

    if importances_for_all_classes:
        importances_for_all_classes_tag.text = str(np.mean(importances_for_all_classes))

    return top


def get_exit_code(results):
    """
    Analyzed recommendation results and generate exit_code for pipeline
    """

    files_analyzed = len(results)
    errors_number = 0
    perfect_code_number = 0
    for result_for_file in results:
        results = result_for_file.get('results')
        errors_string = result_for_file.get('error_string')
        if not results and not errors_string:
            perfect_code_number += 1
        elif not results and errors_string:
            errors_number += 1

    if errors_number == files_analyzed:
        # we have errors everywhere
        exit_code = 2
    elif perfect_code_number == files_analyzed:
        # everything is good
        exit_code = 0
    else:
        # we have some recommendation
        exit_code = 1

    return exit_code


def create_text(results, full_report):
    importances_for_all_classes = []
    buffer = []
    if not full_report:
        buffer.append('Show pattern with the largest contribution to Cognitive Complexity')
    else:
        buffer.append('Show all patterns')
    for result_for_file in results:
        filename = result_for_file.get('filename')
        results = result_for_file.get('results')
        errors_string = result_for_file.get('error_string')
        if not results and not errors_string:
            # Do nothing, patterns were not found
            pass
        if not results and errors_string:
            output_string = '{}: error when calculating patterns: {}'.format(
                filename,
                str(errors_string)
            )
            buffer.append(output_string)
        elif results and not errors_string:
            # get unique patterns score
            patterns_scores = print_total_score_for_file(buffer, filename, importances_for_all_classes, result_for_file)
            patterns_number = len(patterns_scores)
            pattern__number = 0
            cur_pattern_name = ''
            for pattern_item in result_for_file['results']:
                pattern_score = pattern_item.get('importance')
                code = pattern_item.get('pattern_code')
                if code:
                    pattern_name_str = pattern_item.get('pattern_name')
                    if cur_pattern_name != pattern_name_str:
                        pattern__number += 1
                        cur_pattern_name = pattern_name_str
                    buffer.append('{}[{}]: {} ({}: {:.2f} {}/{})'.format(
                        filename,
                        pattern_item.get('code_line'),
                        pattern_name_str,
                        code,
                        pattern_score,
                        pattern__number,
                        patterns_number))
    if importances_for_all_classes:
        buffer.append('Total average score: {}'.format(np.mean(importances_for_all_classes)))

    return buffer


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
    buffer.append('{} score: {}'.format(filename, importances_for_class))
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
        '--threshold',
        help='threshold for predict',
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
        default=[]
    )

    parser.add_argument(
        '--exclude',
        action='append',
        nargs='+'
    )

    args = parser.parse_args(sys.argv[2:])

    if args.suppress:
        args.suppress = args.suppress.strip().split(',')
    if args.threshold:
        print('Threshold for model has been set to {}'.format(args.threshold))

    files_to_exclude = handle_exclude_command_line(args)

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
            text = create_text(new_results, args.full)

            if args.format == 'short':
                print(text[-1])
            else:
                print('\n'.join(text))

    return exit_code


def handle_exclude_command_line(args):
    files_to_exclude = []
    exc_string = 'Usage: --exclude=<glob pattern> ' \
                 '--exclude=<glob pattern> ... ' \
                 '--exclude=folder_to_find_exceptions '
    if args.exclude:
        if len(args.exclude) < 2:
            raise Exception(exc_string)
        try:
            folder_to_exclude = args.exclude[-1][0]
            glob_patterns = [x[0] for x in args.exclude[:-1]]
            for glob_p in glob_patterns:
                files_to_exclude.extend([str(x.absolute()) for x in list(Path(folder_to_exclude).glob(glob_p))])

        except Exception:
            raise Exception(exc_string)
    return files_to_exclude


def format_converter_for_pattern(results, sorted_by=None):
    """Reformat data where data are sorted by patterns importance
    (it is already sorted in the input).
    Then lines are sorted in ascending order."""

    def flatten(l):
        return [item for sublist in l for item in sublist]

    for file in results:
        items = file.get('results')
        if items:
            new_items = flatten([
                [{'pattern_code': x['pattern_code'],
                  'pattern_name': x['pattern_name'],
                  'code_line': line,
                  'importance': x['importance']
                  } for line in sorted(x['code_lines'])] for x in items
            ])
            if not sorted_by:
                file['results'] = sorted(new_items, key=lambda e: (-e['importance'], e['pattern_code'], e['code_line']))
            else:
                file['results'] = sorted(new_items, key=operator.itemgetter(sorted_by, 'pattern_code'))

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
    print('%(prog)s {version}'.format(version=__version__))


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
    releases = json.loads(requests.get(url).content)['releases']
    return sorted(releases, key=parse_version, reverse=True)


def main():
    try:
        max_available_version = get_versions('aibolit')[0]
        if max_available_version != __version__:
            print('Version {} is available, but you are using {}'.format(
                max_available_version,
                __version__
            ))
    except requests.exceptions.ConnectionError:
        print('Can\'t check aibolit version. Network is not available')
    try:
        commands = {
            'train': lambda: train(),
            'check': lambda: check(),
            'recommend': lambda: check(),
            'version': lambda: version(),
        }
        exit_code = run_parse_args(commands)
    except Exception:
        traceback.print_exc()
        sys.exit(2)
    else:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
