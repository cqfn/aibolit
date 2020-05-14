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
    preds = model.predict(np.array(input), th=th)

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
    parser = argparse.ArgumentParser(
        description='Collect dataset and train model'
    )
    parser.add_argument(
        '--java_folder',
        help='full path to directory',
        default=False,
        required=False
    )
    args = parser.parse_args(sys.argv[2:])
    collect_dataset(args.java_folder)
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
        java_file: str,  # type: ignore
        code_lines: List[int],  # type: ignore
        pattern_code: str,  # type: ignore
        pattern_name: str,  # type: ignore
        error_type=None):
    """
    Summarize result and create an output of `predict` function

    :param pattern: pattern name
    :param code_lines: list of code lines where pattern was found
    :param java_file: filename of source Java file
    :patter_code: pattern alias
    :pattern_name: full pattern name
    :return:
    """
    output_string: List[str] = []
    result_item = {
        'output_string': output_string,
        'filename': java_file,
        'pattern_code': pattern_code,
        'pattern_name': pattern_name
    }

    if not code_lines and not error_type:
        output_string.append('Your code is perfect in aibolit\'s opinion')
    elif not code_lines and error_type:
        output_string.append('Error when calculating patterns: {}'.format(str(error_type)))
    else:
        output_str = \
            'The largest contribution for {file} for \"{pattern}\" pattern'.format(
                file=java_file,
                pattern=pattern_name)
        output_string.append(output_str)
        for line in code_lines:
            if line:
                output_string.append('Line {}. Low quality due to: {}'.format(
                    line,
                    pattern_name
                ))
        result_item['code_lines'] = code_lines  # type: ignore

    return result_item


def calculate_patterns_and_metrics(file):
    MI_pipeline_exclude_codes = [
        "M5",  # metric not ready
        "P27",  # empty implementation
    ]
    code_lines_dict = input_params = {}  # type: ignore
    error_string = None
    try:
        config = Config.get_patterns_config()
        for pattern in config['patterns']:
            if pattern in MI_pipeline_exclude_codes:
                continue
            __count_value(pattern, input_params, code_lines_dict, file)

        for metric in config['metrics']:
            if metric in MI_pipeline_exclude_codes:
                continue
            __count_value(metric, input_params, code_lines_dict, file, is_metric=True)
    except Exception as ex:
        error_string = str(ex)
        input_params = []  # type: ignore

    return input_params, code_lines_dict, error_string


def inference(input_params: List[int], code_lines_dict, args):
    """
    Find a pattern which has the largest impact on target

    :param input_params: list if calculated patterns/metrics
    :param code_lines_dict: list with found code lines of patterns/metrics
    :return:
    """
    model_path = args.model_file
    if input_params:
        if not model_path:
            model_path = Config.folder_model_data()
        with open(model_path, 'rb') as fid:
            model = pickle.load(fid)
        sorted_result = predict(input_params, model, args)
        code_lines = None
        patterns_list = model.features_conf['patterns_only']
        pattern_code = None  # type: ignore
        for iter, (key, val) in enumerate(sorted_result.items()):
            if key in patterns_list:
                pattern_code = key
                code_lines = code_lines_dict.get('lines_' + key)
                # We show only positive gradient, we won't add patterns
                if code_lines and val > 1.00000e-20:
                    break

        if code_lines:
            pattern_name = [x['name'] for x in Config.get_patterns_config()['patterns'] if x['code'] == pattern_code][0]
        else:
            pattern_name = None
            pattern_code = None
            code_lines = []
    else:
        code_lines = []
        pattern_code = None  # type: ignore
        pattern_name = None

    return code_lines, pattern_code, pattern_name


def run_recommend_for_file(file: str, args):
    """
    Calculate patterns and metrics, pass values to model and recommend pattern to change
    :param file: file to analyze
    :param args: different command line arguments
    :return: dict with code lines, filename and pattern name
    """
    print('Analyzing {}'.format(file))
    java_file = str(Path(os.getcwd(), file))
    input_params, code_lines_dict, error_string = calculate_patterns_and_metrics(java_file)
    code_lines, pattern_code, pattern_name = inference(input_params, code_lines_dict, args)

    return create_output(
        java_file=java_file,  # type: ignore
        code_lines=code_lines,  # type: ignore
        pattern_code=pattern_code,  # type: ignore
        pattern_name=pattern_name,  # type: ignore
        error_type=error_string  # type: ignore
    )


def create_xml_tree(results):
    """
    Creates xml from output of `recommend` function
    :param results: output of `recommend` function
    :return: xml string
    """

    top = etree.Element('files')
    for result in results:
        child = etree.SubElement(top, 'filename')
        child.text = result.get('filename')
        if result.get('pattern_code'):
            pattern_item = etree.SubElement(child, 'pattern')
            pattern_item.text = result.get('pattern_name') or ''
            pattern_item.attrib['pattern_code'] = result.get('pattern_code')
        output_string = etree.SubElement(child, 'output_string')
        output_string.text = '\n'.join(result['output_string'])

        code_lines_items = result.get('code_lines')
        if code_lines_items:
            code_lines_lst_tree_node = etree.SubElement(child, 'code_lines')
            for code_line in code_lines_items:
                code_line_elem = etree.SubElement(code_lines_lst_tree_node, 'line_number')
                code_line_elem.text = str(code_line)

    return top


def recommend():
    """Run recommendation pipeline."""

    parser = argparse.ArgumentParser(
        description='Get recommendations for Java code',
        usage='''
        aibolit recommend < --folder | --filenames > [--output] [--model_file] [--threshold]
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
        '--output',
        help='output of xml file where all results will be saved, default is out.xml of the current directory',
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

    # make a certain order of arguments which was used by a model

    args = parser.parse_args(sys.argv[2:])

    if args.threshold:
        print('Threshold for model has been set to {}'.format(args.threshold))

    if args.filenames:
        files = args.filenames
    elif args.folder:
        files = []
        list_dir(args.folder, files)

    results = list(run_thread(files, args))

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
