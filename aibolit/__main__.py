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
import os
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

import torch

from aibolit import __version__
from aibolit.metrics.entropy.entropy import Entropy
from aibolit.metrics.ncss.ncss import NCSSMetric
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter
from aibolit.model.model import Net  # type: ignore
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

dir_path = os.path.dirname(os.path.realpath(__file__))


def find_halstead(java_file):
    halstead_binary_path = Path(dir_path, 'binary_files/halstead.jar')
    cmd = ['java', '-jar', str(halstead_binary_path), java_file]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    score = None
    if not err:
        score = float(out.decode().split('readability:')[-1].strip())
    else:
        raise Exception('Error when running: {}'.format(err))
    return score


def predict(input_params):
    # make a certain order of arguments which was used by a model
    features_order = [
        'var_middle_number', 'this_find_number', 'string_concat_number',
        'instance_of_number', 'method_chain_number', 'var_decl_diff_number_11',
        'var_decl_diff_number_7', 'var_decl_diff_number_5',
        'super_method_call_number', 'force_type_cast_number', 'asserts_number',
        'setter_number', 'empty_rethrow_number',
        'prohibited_class_names_number', 'return_in_if_number',
        'impl_multi_number', 'many_prim_ctors_number', 'multiple_try_number',
        'non_final_field_number', 'null_check_number', 'part_sync_number',
        'red_catch_number', 'return_null_number'
    ]

    # load model to cpu
    model = Net()
    model_path = Path(dir_path, 'binary_files/model.dat')
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()

    input = [input_params[i] for i in features_order]
    x = torch.FloatTensor(input)

    # Run model, return gradient and return list of patterns
    x.requires_grad_(True)
    out = model(x)
    out.backward()
    results = x.grad
    sorted_result = OrderedDict(
        sorted(
            dict(zip(features_order, results.numpy().tolist())).items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
    )
    return sorted_result


# flake8: noqa
def main():
    exit_status = -1
    patterns_list = [
        'var_middle_number', 'this_find_number', 'string_concat_number', 'instance_of_number',
        'method_chain_number', 'var_decl_diff_number_11', 'var_decl_diff_number_7', 'var_decl_diff_number_5',
        'super_method_call_number', 'force_type_cast_number', 'asserts_number', 'setter_number', 'empty_rethrow_number',
        'prohibited_class_names_number', 'return_in_if_number', 'impl_multi_number',
        'many_prim_ctors_number', 'multiple_try_number', 'non_final_field_number', 'null_check_number',
        'part_sync_number', 'red_catch_number', 'return_null_number'
    ]
    try:
        parser = argparse.ArgumentParser(
            description='Find the pattern which has the largest impact on readability'
        )
        parser.add_argument(
            '--filename',
            help='path for Java file')
        parser.add_argument('--version', action='version',
                            version='%(prog)s {version}'.format(version=__version__))

        args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

        if args:
            java_file = str(Path(os.getcwd(), args.filename))
            halstead_volume = find_halstead(java_file)
            var_numbers = VarMiddle().value(java_file)
            entropy = Entropy().value(java_file)
            left_space_variance, right_space_variance, max_left_space_diff, max_right_space_diff \
                = IndentationCounter().value(java_file)
            concat_str_number = StringConcatFinder().value(java_file)
            instance_of_lines = InstanceOf().value(java_file)
            method_chain_lines = MethodChainFind().value(java_file)
            var_decl_diff_lines_5 = VarDeclarationDistance(lines_th=5).value(java_file)
            var_decl_diff_lines_7 = VarDeclarationDistance(lines_th=7).value(java_file)
            var_decl_diff_lines_11 = VarDeclarationDistance(lines_th=11).value(java_file)
            super_m_lines = SuperMethod().value(java_file)
            force_type_cast_number = ForceTypeCastingFinder().value(java_file)
            this_lines = ThisFinder().value(java_file)
            asserts_lines = AssertInCode().value(java_file)
            setter_lines = ClassicSetter().value(java_file)
            empty_rethrow_lines = EmptyRethrow().value(java_file)
            prohibited_class_names = ErClass().value(java_file)
            if_return_lines = CountIfReturn().value(java_file)
            impl_multi_lines = ImplementsMultiFinder().value(java_file)
            many_prim_ctors_lines = ManyPrimaryCtors().value(java_file)
            multiple_try_lines = MultipleTry().value(java_file)
            non_final_field_lines = NonFinalAttribute().value(java_file)
            null_check_lines = NullCheck().value(java_file)
            part_sync_lines = PartialSync().value(java_file)
            red_catch_lines = RedundantCatch().value(java_file)
            return_null_lines = ReturnNull().value(java_file)
            ncss_lightweight = NCSSMetric(java_file).value()

            code_lines_dict = {
                'var_middle_number': var_numbers,
                'string_concat_number': concat_str_number,
                'instance_of_number': instance_of_lines,
                'method_chain_number': method_chain_lines,
                'var_decl_diff_number_5': var_decl_diff_lines_5,
                'var_decl_diff_number_7': var_decl_diff_lines_7,
                'var_decl_diff_number_11': var_decl_diff_lines_11,
                'super_method_call_number': super_m_lines,
                'force_type_cast_number': force_type_cast_number,
                'this_find_number': this_lines,
                'asserts_number': asserts_lines,
                'setter_number': setter_lines,
                'empty_rethrow_number': empty_rethrow_lines,
                'prohibited_class_names_number': prohibited_class_names,
                'return_in_if_number': if_return_lines,
                'impl_multi_number': impl_multi_lines,
                'many_prim_ctors_number': many_prim_ctors_lines,
                'multiple_try_number': multiple_try_lines,
                'non_final_field_number': non_final_field_lines,
                'null_check_number': null_check_lines,
                'part_sync_number': part_sync_lines,
                'red_catch_number': red_catch_lines,
                'return_null_number': return_null_lines,
            }
            input_params = {
                'var_middle_number': len(var_numbers),
                'string_concat_number': len(concat_str_number),
                'instance_of_number': len(instance_of_lines),
                'method_chain_number': len(method_chain_lines),
                'var_decl_diff_number_5': len(var_decl_diff_lines_5),
                'var_decl_diff_number_7': len(var_decl_diff_lines_7),
                'var_decl_diff_number_11': len(var_decl_diff_lines_11),
                'super_method_call_number': len(super_m_lines),
                'force_type_cast_number': len(force_type_cast_number),
                'this_find_number': len(this_lines),
                'asserts_number': len(asserts_lines),
                'setter_number': len(setter_lines),
                'empty_rethrow_number': len(empty_rethrow_lines),
                'prohibited_class_names_number': len(prohibited_class_names),
                'return_in_if_number': len(if_return_lines),
                'impl_multi_number': len(impl_multi_lines),
                'many_prim_ctors_number': len(many_prim_ctors_lines),
                'multiple_try_number': len(multiple_try_lines),
                'non_final_field_number': len(non_final_field_lines),
                'null_check_number': len(null_check_lines),
                'part_sync_number': len(part_sync_lines),
                'red_catch_number': len(red_catch_lines),
                'return_null_number': len(return_null_lines),
                'entropy': entropy,
                'halstead volume': halstead_volume,
                'left_spaces_var': left_space_variance,
                'right_spaces_var': right_space_variance,
                'max_left_diff_spaces': max_left_space_diff,
                'max_right_diff_spaces': max_right_space_diff,
                'ncss_lightweight': ncss_lightweight,
            }

            sorted_result = predict(input_params)
            found_pattern = False
            code_lines = None
            value = None
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
            exit_status = 0
    except KeyboardInterrupt:
        exit_status = -1
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
