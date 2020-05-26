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
import multiprocessing
import sys
from os import scandir
from typing import List

from lxml import etree  # type: ignore
import numpy as np  # type: ignore
from aibolit import __version__
from aibolit.config import Config
from aibolit.ml_pipeline.ml_pipeline import train_process, collect_dataset
import os
from pathlib import Path
import pickle
from aibolit.model.model import TwoFoldRankingModel, Dataset  # type: ignore  # noqa: F401
from sys import stdout

dir_path = os.path.dirname(os.path.realpath(__file__))


def list_dir(path, files):
    dir_list = []
    for entry in scandir(path):
        if entry.is_dir():
            dir_list.append(entry.path)
            dir_list.extend(list_dir(entry.path, files))
        elif entry.is_file() and entry.path.endswith('.java'):
            files.append(entry.path)
    return dir_list


def predict(input_params, model, args):
    features_order = model.features_conf['features_order']
    # load model
    input = [input_params[i] for i in features_order]
    th = float(args.threshold) or 1.0
    preds, importances = model.predict(np.array(input), th=th)

    return {features_order[int(x)]: int(x) for x in preds.tolist()[0]}, importances


def run_parse_args(commands_dict):
    parser = argparse.ArgumentParser(
        description='Find the pattern which has the largest impact on readability',
        usage='''
        aibolit <command> [<args>]

        You can run 1 command:
        train          Train model
        recommend      Recommend pattern
        ''')

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


def calculate_patterns_and_metrics(file):
    code_lines_dict = input_params = {}  # type: ignore
    error_string = None
    try:
        config = Config.get_patterns_config()
        for pattern in config['patterns']:
            if pattern['code'] in config['patterns_exclude']:
                continue
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
    model_path = args.model_file
    do_full_report = args.full
    results = []
    importances = [-1]
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
                # We show only patterns with positive importance
                if code_lines and val > 1.00000e-20:
                    if code_lines:
                        pattern_name = \
                            [x['name'] for x in Config.get_patterns_config()['patterns']
                             if x['code'] == pattern_code][0]
                        results.append(
                            {'code_lines': code_lines,
                             'pattern_code': pattern_code,
                             'pattern_name': pattern_name
                             })
                    if not do_full_report:
                        break
    else:
        return results, sum(importances)

    return results, sum(importances)


def run_recommend_for_file(file: str, args):
    """
    Calculate patterns and metrics, pass values to model and recommend pattern to change
    :param file: file to analyze
    :param args: different command line arguments
    :return: dict with code lines, filename and pattern name
    """
    java_file = str(Path(os.getcwd(), file))
    input_params, code_lines_dict, error_string = calculate_patterns_and_metrics(java_file)
    results_list, importances = inference(input_params, code_lines_dict, args)

    return {
        'filename': file,
        'results': results_list,
        'error_string': error_string,
        'importances': importances
    }


def create_xml_tree(results, full_report):
    """
    Creates xml from output of `recommend` function
    :param results: output of `recommend` function
    :return: xml string
    """
    importances_for_all_classes = []
    top = etree.Element('report')
    importances_for_all_classes_tag = etree.SubElement(top, 'score')
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
            importances_value_per_class = result_for_file['importances']
            importances_sum_tag.text = str(importances_value_per_class)
            importances_for_all_classes.append(importances_value_per_class)
            patterns_tag = etree.SubElement(file, 'patterns')
            for pattern in result_for_file['results']:
                if pattern.get('pattern_code'):
                    pattern_item = etree.SubElement(patterns_tag, 'pattern')
                    pattern_name_str = pattern.get('pattern_name')
                    details = etree.SubElement(pattern_item, 'details')
                    details.text = pattern_name_str or ''
                    pattern_item.attrib['code'] = pattern.get('pattern_code')
                    code_lines_items = pattern.get('code_lines')
                    if code_lines_items:
                        code_lines_lst_tree_node = etree.SubElement(pattern_item, 'lines')
                        for code_line in code_lines_items:
                            code_line_elem = etree.SubElement(code_lines_lst_tree_node, 'number')
                            code_line_elem.text = str(code_line)
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
        buffer.append('Filename {}: '.format(filename))
        results = result_for_file.get('results')
        errors_string = result_for_file.get('error_string')
        if not results and not errors_string:
            output_string = 'Your code is perfect in aibolit\'s opinion'
            buffer.append(output_string)
        elif not results and errors_string:
            output_string = 'Error when calculating patterns: {}'.format(str(errors_string))
            buffer.append(output_string)
        else:
            output_string = 'Some issues found'
            score = result_for_file['importances']
            importances_for_all_classes.append(score)
            buffer.append('Score for file: {}'.format(score))
            buffer.append(output_string)
            for pattern_item in result_for_file['results']:
                code = pattern_item.get('pattern_code')
                if code:
                    pattern_name_str = pattern_item.get('pattern_name')
                    buffer.append('line {}: {} ({})'.format(pattern_item.get('code_line'), pattern_name_str, code))
    if importances_for_all_classes:
        buffer.append('Total score: {}'.format(np.mean(importances_for_all_classes)))

    return buffer


def recommend():
    """Run recommendation pipeline."""

    parser = argparse.ArgumentParser(
        description='Get recommendations for Java code',
        usage='''
        aibolit recommend < --folder | --filenames > [--output] [--model_file] [--threshold] [--full] [--format]
        ''')

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
        '--model_file',
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
        default='text',
        help='text (by default) or xml. Usage: --format=xml'
    )

    args = parser.parse_args(sys.argv[2:])

    if args.threshold:
        print('Threshold for model has been set to {}'.format(args.threshold))

    if args.filenames:
        files = args.filenames
    elif args.folder:
        files = []
        list_dir(args.folder, files)

    results = list(run_thread(files, args))

    if args.format:
        new_results = format_converter_for_pattern(results)
        if args.format == 'text':
            text = create_text(new_results, args)
            print('\n'.join(text))
        elif args.format == 'xml':
            root = create_xml_tree(results, args.full)
            tree = root.getroottree()
            tree.write(stdout.buffer, pretty_print=True)
        else:
            raise Exception('Unknown format')

    exit_code = get_exit_code(results)
    return exit_code


def format_converter_for_pattern(results):
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
                  } for line in sorted(x['code_lines'])] for x in items
            ])
            file['results'] = new_items

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


def main():
    try:
        commands = {
            'train': lambda: train(),
            'recommend': lambda: recommend(),
            'version': lambda: version(),
        }
        exit_code = run_parse_args(commands)
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(2)
    else:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
