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
import sys
from pathlib import Path
from collections import OrderedDict
import json
from aibolit import __version__
from aibolit.metrics.entropy.entropy import Entropy
from aibolit.metrics.ncss.ncss import NCSSMetric
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter
from aibolit.ml_pipeline.ml_pipeline import *
from aibolit.patterns.assert_in_code.assert_in_code import AssertInCode
from aibolit.patterns.classic_setter.classic_setter import ClassicSetter
from aibolit.patterns.empty_rethrow.empty_rethrow import EmptyRethrow
from aibolit.patterns.er_class.er_class import ErClass
from aibolit.patterns.force_type_casting_finder.force_type_casting_finder import ForceTypeCastingFinder
from aibolit.patterns.if_return_if_detection.if_detection import CountIfReturn
from aibolit.patterns.implements_multi.implements_multi import ImplementsMultiFinder
from aibolit.patterns.instanceof.instance_of import InstanceOf
from aibolit.patterns.many_primary_ctors.many_primary_ctors import ManyPrimaryCtors
from aibolit.patterns.method_chaining.method_chaining import MethodChainFind
from aibolit.patterns.multiple_try.multiple_try import MultipleTry
from aibolit.patterns.non_final_attribute.non_final_attribute import NonFinalAttribute
from aibolit.patterns.null_check.null_check import NullCheck
from aibolit.patterns.partial_synchronized.partial_synchronized import PartialSync
from aibolit.patterns.redundant_catch.redundant_catch import RedundantCatch
from aibolit.patterns.return_null.return_null import ReturnNull
from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.patterns.supermethod.supermethod import SuperMethod
from aibolit.patterns.this_finder.this_finder import ThisFinder
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance
from aibolit.patterns.var_middle.var_middle import VarMiddle
from aibolit.metrics.ncss.ncss import NCSSMetric
from aibolit.config import CONFIG

dir_path = os.path.dirname(os.path.realpath(__file__))


def predict(input_params, features_conf):
    features_order = features_conf['features_order']
    # load model
    input = [input_params[i] for i in features_order]
    cwd = Path(os.getcwd())
    print('Current cmd: ' + str(cwd))
    model_path = Path(dir_path, 'binary_files/model.pkl')

    with open(model_path, 'rb') as fid:
        model_new = pickle.load(fid)
        preds = model_new.predict(input)
        print(preds)

    sorted_result = OrderedDict(
        sorted(
            dict(zip(features_order, preds)).items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
    )
    return sorted_result


class CLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Find the pattern which has the largest impact on readability',
            usage='''aibolit <command> [<args>]

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
        if not hasattr(self, args.command):
            parser.print_help()
            exit(1)

        getattr(self, args.command)()

    def train(self):
        # collect_dataset()
        train_process()

    def __count_value(self, value_dict, input_params, code_lines_dict, java_file: str, is_metric=False):
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

    # flake8: noqa: C901
    def recommend(self):
        parser = argparse.ArgumentParser(
            description='Download objects and refs from another repository')
        parser.add_argument(
            'recommend',
            help='path for Java file',
            nargs="*",
            default=False
        )
        # make a certain order of arguments which was used by a model
        with open('binary_files/features_order.json', 'r', encoding='utf-8') as f:
            features_conf = json.load(f)

        args = parser.parse_args(sys.argv[2:])
        for file in args.recommend:
            print('Analyzing {}'.format(file))
            java_file = str(Path(os.getcwd(), file))
            code_lines_dict = input_params = {}
            for pattern in CONFIG['patterns']:
                self.__count_value(pattern, input_params, code_lines_dict, java_file)

            for metric in CONFIG['metrics']:
                self.__count_value(metric, input_params, code_lines_dict, java_file, is_metric=True)

            sorted_result = predict(input_params, features_conf)
            found_pattern = False
            code_lines = None
            value = None
            patterns_list = features_conf['patterns_list']
            for iter, (key, val) in enumerate(sorted_result.items()):
                if key in patterns_list:
                    if not found_pattern:
                        pattern = key
                        code_lines = code_lines_dict.get(key)
                        # We show only positive gradient, we won't add patterns
                        if code_lines and val > 1.00000e-20:
                            found_pattern = True
                            value = val

            if not code_lines:
                print('Your code is perfect in aibolit\'s opinion')
            else:
                output_str = \
                    'The largest contribution for {file} is {val} for \"{pattern}\" pattern'.format(
                        file=java_file,
                        pattern=pattern,
                        val=value)
                print(output_str)
                for line in code_lines:
                    if line:
                        print('Line {}. Low readability due to: {}'.format(
                            line,
                            pattern
                        ))

    def version(self):
        parser = argparse.ArgumentParser(
            description='Show version')
        parser.add_argument(
            '--version',
        )
        print('%(prog)s {version}'.format(version=__version__))


def main():
    exit_status = -1
    try:
        CLI()
    except KeyboardInterrupt:
        exit_status = -1
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
