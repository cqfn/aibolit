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
from pathlib import Path

from aibolit import __version__
from aibolit.metrics.entropy.entropy import Entropy
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter
from aibolit.patterns.force_type_casting_finder.force_type_casting_finder import ForceTypeCastingFinder
from aibolit.patterns.instanceof.instance_of import InstanceOf
from aibolit.patterns.method_chaining.method_chaining import MethodChainFind
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.patterns.supermethod.supermethod import SuperMethod
from aibolit.patterns.this_finder.this_finder import ThisFinder
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance
from aibolit.patterns.var_middle.var_middle import VarMiddle

dir_path = os.path.dirname(os.path.realpath(__file__))


def find_halstead(java_file):
    halstead_binary_path = Path(dir_path, 'binary_files/halstead.jar')
    cmd = ['java', '-jar', halstead_binary_path, java_file]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    score = None
    if not err:
        score = float(out.decode().split('readability:')[-1].strip())
    else:
        raise Exception('Error when running: {}'.format(err))
    return score


def find_ncss(java_file):
    return 0


def predict(input_params):
    # make a certain order of arguments
    # pass it to model
    # Run model, return gradient and return list of patterns
    return ['var_middle', 'string_concat']


def main():
    exit_status = -1
    patterns_dict = {
        'var_middle': VarMiddle(),
        'string_concat': StringConcatFinder()
    }
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
            ncss_value = find_ncss(java_file)
            var_numbers = VarMiddle().value(java_file)
            nested_for_blocks = NestedBlocks(2, block_type=BlockType.FOR).value(java_file)
            nested_if_blocks = NestedBlocks(2, block_type=BlockType.IF).value(java_file)
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
            for_type_cast_lines = ForceTypeCastingFinder().value(java_file)
            this_lines = ThisFinder().value(java_file)
            print(halstead_volume)
            input_params = {
                'halstead volume': halstead_volume,
                'ncss_avg': ncss_value,
                'var_middle_number': len(var_numbers),
                'nested_for_number': len(nested_for_blocks),
                'nested_if_number': len(nested_if_blocks),
                'string_concat_number': len(concat_str_number),
                'instance_of_number': len(instance_of_lines),
                'method_chain_number': len(method_chain_lines),
                'var_decl_diff_number_5': len(var_decl_diff_lines_5),
                'var_decl_diff_number_7': len(var_decl_diff_lines_7),
                'var_decl_diff_number_11': len(var_decl_diff_lines_11),
                'super_method_call_number': len(super_m_lines),
                'for_type_cast_number': len(for_type_cast_lines),
                'this_find_number': len(this_lines),
                'entropy': entropy,
                'left_spaces_var': left_space_variance,
                'right_spaces_var': right_space_variance,
                'max_left_diff_spaces': max_left_space_diff,
                'max_right_diff_spaces': max_right_space_diff,
            }

            order_queue = predict(input_params)
            pattern_name = order_queue[0]
            pattern = patterns_dict.get(pattern_name)
            lines = pattern.value(java_file)
            if not lines:
                print('Your code is perfect in aibolit\'s opinion')
            for line in lines:
                if line:
                    print('Line {}. Low readability due to: {}'.format(
                        line,
                        pattern_name
                    ))
            exit_status = 0
    except KeyboardInterrupt:
        exit_status = -1
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
