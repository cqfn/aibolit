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

from lxml import etree
import numpy as np
from aibolit import __version__
from aibolit.config import CONFIG
from aibolit.ml_pipeline.ml_pipeline import train_process, collect_dataset
import os
from pathlib import Path
import pickle
import json

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


def predict(input_params, features_conf):
    features_order = features_conf['features_order']
    # load model
    input = [input_params[i] for i in features_order]
    cwd = Path(os.getcwd())
    print('Current cmd: ' + str(cwd))
    model_path = Path(dir_path, 'binary_files/model.pkl')

    with open(model_path, 'rb') as fid:
        model_new = pickle.load(fid)
        preds = model_new.predict(np.array(input))

    return {features_order[int(x)]: x for x in preds.tolist()[0]}


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

    commands_dict[args.command]()


def train():
    # collect_dataset()
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


def create_output(
        java_file: str,
        code_lines: List[int],
        pattern_code: str,
        pattern_name: str):
    """
    Summarize result and create an output of `predict` function

    :param pattern: pattern name
    :param code_lines: list of code lines where pattern was found
    :param java_file: filename of source Java file
    :patter_code: pattern alias
    :pattern_name: full pattern name
    :return:
    """
    output_string = []
    result_item = {
        'output_string': output_string,
        'filename': java_file,
        'pattern_code': pattern_code,
        'pattern_name': pattern_name
    }

    if not code_lines:
        output_string.append('Your code is perfect in aibolit\'s opinion')
    else:
        output_str = \
            'The largest contribution for {file} for \"{pattern}\" pattern'.format(
                file=java_file,
                pattern=pattern_name)
        output_string.append(output_str)
        for line in code_lines:
            if line:
                output_string.append('Line {}. Low readability due to: {}'.format(
                    line,
                    pattern_name
                ))
        result_item['code_lines'] = code_lines

    return result_item


def run_recommend_for_file(file: str, features_conf: dict):
    """
    Calculate patterns and metrics, pass values to model and recommend pattern to change
    :param file: file to analyze
    :param features_conf: dict from features_order.json in repo
    :return: dict with code lines, filename and pattern name
    """
    print('Analyzing {}'.format(file))
    MI_pipeline_exclude_codes = [
        "M5",  # metric not ready
        "P27",  # empty implementation
    ]
    java_file = str(Path(os.getcwd(), file))
    code_lines_dict = input_params = {}
    for pattern in CONFIG['patterns']:
        if pattern in MI_pipeline_exclude_codes:
            continue
        __count_value(pattern, input_params, code_lines_dict, java_file)

    for metric in CONFIG['metrics']:
        if metric in MI_pipeline_exclude_codes:
            continue
        __count_value(metric, input_params, code_lines_dict, java_file, is_metric=True)

    sorted_result = predict(input_params, features_conf)
    code_lines = None
    patterns_list = features_conf['patterns_only']
    pattern = None
    for iter, (key, val) in enumerate(sorted_result.items()):
        if key in patterns_list:
            pattern = key
            code_lines = code_lines_dict.get('lines_' + key)
            # We show only positive gradient, we won't add patterns
            if code_lines and val > 1.00000e-20:
                break

    pattern_name = [x['name'] for x in CONFIG['patterns'] if x['code'] == pattern][0]
    return create_output(
        java_file=java_file,
        code_lines=code_lines,
        pattern_code=pattern,
        pattern_name=pattern_name
    )


def create_xml_tree(results):
    """
    Creates xml from output of `recommend` function
    :param results: output of `recommend` function
    :return: xml string
    """

    top = etree.Element('files')
    for result in results:
        comment = etree.Comment('All processed files')
        top.append(comment)

        child = etree.SubElement(top, 'filename')
        child.text = result['filename']
        code_lines_list = etree.SubElement(child, 'code_lines')
        pattern_item = etree.SubElement(child, 'pattern')
        pattern_item.text = result['pattern_name']
        pattern_item.attrib['pattern_code'] = result['pattern_code']
        pattern_item = etree.SubElement(child, 'output_string')
        pattern_item.text = '\n'.join(result['output_string'])

        for code_line in result['code_lines']:
            code_line_elem = etree.SubElement(code_lines_list, 'line_number')
            code_line_elem.text = str(code_line)

    return top


def recommend():
    """Run recommendation pipeline."""

    parser = argparse.ArgumentParser(
        description='Download objects and refs from another repository')
    parser.add_argument(
        '--folder',
        help='path to Java files',
        default=False
    )
    parser.add_argument(
        '--filenames',
        help='Java files',
        nargs="*",
        default=False
    )
    parser.add_argument(
        '--output',
        help='output file for results',
        default=False
    )
    # make a certain order of arguments which was used by a model
    with open('binary_files/features_order.json', 'r', encoding='utf-8') as f:
        features_conf = json.load(f)

    args = parser.parse_args(sys.argv[2:])
    results = []
    if args.filenames:
        results = list(run_thread(args.filenames, features_conf))
    elif args.folder:
        files = []
        list_dir(args.folder, files)
        results = list(run_thread(files, features_conf))

    if args.output:
        filename = args.output
    else:
        filename = 'out.xml'

    root = create_xml_tree(results)
    tree = root.getroottree()
    tree.write(filename, pretty_print=True)


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


def run_thread(files, features_conf):
    """
    Parallel patterns/metrics calculation
    :param files: list of java files to analyze
    :param features_conf: dict from features_order.json in repo

    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        future_results = [executor.submit(run_recommend_for_file, file, features_conf) for file in files]
        concurrent.futures.wait(future_results)
        for future in future_results:
            yield future.result()


def main():
    exit_status = 0
    try:
        commands = {
            'train': lambda: train(),
            'recommend': lambda: recommend(),
            'version': lambda: version(),
        }
        run_parse_args(commands)

    except KeyboardInterrupt:
        exit_status = -1
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
