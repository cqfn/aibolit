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

import argparse
import csv
import os
import time
from functools import partial
from multiprocessing import Pool
from pathlib import Path

from aibolit.metrics.entropy.entropy import Entropy
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.instanceof.instance_of import InstanceOf
from aibolit.patterns.method_chaining.method_chaining import MethodChainFind
from aibolit.patterns.var_decl_diff.var_decl_diff import VarDeclarationDistance
from aibolit.patterns.supermethod.supermethod import SuperMethod
from aibolit.patterns.force_type_casting_finder.force_type_casting_finder import ForceTypeCastingFinder
from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.patterns.var_middle.var_middle import VarMiddle

parser = argparse.ArgumentParser(description='Find patterns in Java files')
parser.add_argument(
    '--filename',
    help='path for file with a list of Java files',
    required=True)

args = parser.parse_args()
dir_path = os.path.dirname(os.path.realpath(__file__))


def log_result(result, file_to_write):
    """ Save result to csv file. """
    with open(file_to_write, 'a', newline='\n', encoding='utf-8') as csv_file:
        fieldnames = [
            'filename', 'var_middle_number', 'nested_for_number',
            'nested_if_number', 'string_concat_number', 'instance_of_number',
            'method_chain_number', 'var_decl_diff_number', 'super_method_call_number',
            'for_type_cast_number', 'lines_instance_of_number', 'lines_method_chain_number',
            'lines_var_decl_diff_number', 'lines_super_method_call_number',
            'lines_for_type_cast_number', 'lines_string_concat',
            'lines_for_var_middle', 'lines_for_cycle', 'lines_for_if', 'entropy',
            'left_spaces_var', 'right_spaces_var', 'max_left_diff_spaces', 'max_right_diff_spaces'
        ]
        writer = csv.DictWriter(
            csv_file, delimiter=';',
            quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=fieldnames)
        writer.writerow(result)


def execute_python_code_in_parallel_thread(file):
    """ This runs in a separate thread. """
    var_numbers = VarMiddle().value(file)
    nested_for_blocks = NestedBlocks(2, block_type=BlockType.FOR).value(file)
    nested_if_blocks = NestedBlocks(2, block_type=BlockType.IF).value(file)
    entropy = Entropy().value(file)
    left_space_variance, right_space_variance, max_left_space_diff, max_right_space_diff \
        = IndentationCounter().value(file)
    concat_str_number = StringConcatFinder().value(file)
    instance_of_lines = InstanceOf().value(file)
    method_chain_lines = MethodChainFind().value(file)
    var_decl_diff_lines = VarDeclarationDistance().value(file)
    super_m_lines = SuperMethod().value(file)
    for_type_cast_lines = ForceTypeCastingFinder.value(file)
    p = Path(file)
    d_path = Path(dir_path)
    relative_path = p.relative_to(d_path)

    return {
        'filename': relative_path.as_posix(),
        # lines number
        'var_middle_number': len(var_numbers),
        'nested_for_number': len(nested_for_blocks),
        'nested_if_number': len(nested_if_blocks),
        'string_concat_number': len(concat_str_number),
        'instance_of_number': len(instance_of_lines),
        'method_chain_number': len(method_chain_lines),
        'var_decl_diff_number': len(var_decl_diff_lines),
        'super_method_call_number': len(super_m_lines),
        'for_type_cast_number': len(for_type_cast_lines),
        # lines info about feature location
        'lines_instance_of_number': instance_of_lines,
        'lines_method_chain_number': method_chain_lines,
        'lines_var_decl_diff_number': var_decl_diff_lines,
        'lines_super_method_call_number': super_m_lines,
        'lines_for_type_cast_number': for_type_cast_lines,
        'lines_string_concat': concat_str_number,
        'lines_for_var_middle': var_numbers,
        'lines_for_cycle': nested_for_blocks,
        'lines_for_if': nested_if_blocks,
        # some numerical characteristics
        'entropy': entropy,
        'left_spaces_var': left_space_variance,
        'right_spaces_var': right_space_variance,
        'max_left_diff_spaces': max_left_space_diff,
        'max_right_diff_spaces': max_right_space_diff,
    }
    # file, var_numbers, nested_for_blocks, nested_if_blocks, entropy, \
    #        spaces, concat_str_number, instance_of_lines


if __name__ == '__main__':
    start = time.time()

    path = 'target/04'
    os.makedirs(path, exist_ok=True)
    filename = 'target/04/04-find-patterns.csv'

    pool = Pool(20)
    handled_files = []
    log_func = partial(log_result, file_to_write=filename)
    with open(args.filename, 'r') as f:
        for i in f.readlines():
            java_file = str(Path(dir_path, i)).strip()
            pool.apply_async(
                execute_python_code_in_parallel_thread,
                args=(java_file,),
                callback=log_func)

    pool.close()
    pool.join()

    end = time.time()
    print('It took {} seconds'.format(str(end - start)))