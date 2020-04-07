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
import multiprocessing
import os
import time
import traceback
from functools import partial
from pathlib import Path
import sys
from multiprocessing import Manager

from aibolit.metrics.entropy.entropy import Entropy
from aibolit.metrics.spaces.SpaceCounter import IndentationCounter
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
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
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
        writer = csv.DictWriter(
            csv_file, delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            fieldnames=list(result.keys()))
        writer.writerow(result)


def execute_python_code_in_parallel_thread(exceptions, file_local_dir):
    """ This runs in a separate thread. """
    try:
        file = str(Path(dir_path, file_local_dir)).strip()
        var_numbers = VarMiddle().value(file)
        nested_for_blocks = NestedBlocks(2, block_type=BlockType.FOR).value(file)
        nested_if_blocks = NestedBlocks(2, block_type=BlockType.IF).value(file)
        entropy = Entropy().value(file)
        left_space_variance, right_space_variance, max_left_space_diff, max_right_space_diff \
            = IndentationCounter().value(file)
        concat_str_number = StringConcatFinder().value(file)
        instance_of_lines = InstanceOf().value(file)
        method_chain_lines = MethodChainFind().value(file)
        var_decl_diff_lines_5 = VarDeclarationDistance(lines_th=5).value(file)
        var_decl_diff_lines_7 = VarDeclarationDistance(lines_th=7).value(file)
        var_decl_diff_lines_11 = VarDeclarationDistance(lines_th=11).value(file)
        super_m_lines = SuperMethod().value(file)
        for_type_cast_lines = ForceTypeCastingFinder().value(file)
        this_lines = ThisFinder().value(file)
        asserts_lines = AssertInCode().value(file)
        setter_lines = ClassicSetter().value(file)
        empty_rethrow_lines = EmptyRethrow().value(file)
        prohibited_class_names = ErClass().value(file)
        if_return_lines = CountIfReturn().value(file)
        impl_multi_lines = ImplementsMultiFinder().value(file)
        many_prim_ctors_lines = ManyPrimaryCtors().value(file)
        multiple_try_lines = MultipleTry().value(file)
        non_final_field_lines = NonFinalAttribute().value(file)
        null_check_lines = NullCheck().value(file)
        part_sync_lines = PartialSync().value(file)
        red_catch_lines = RedundantCatch().value(file)
        return_null_lines = ReturnNull().value(file)
        ncss_lightweight = NCSSMetric(file).value()
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
            'var_decl_diff_number_5': len(var_decl_diff_lines_5),
            'var_decl_diff_number_7': len(var_decl_diff_lines_7),
            'var_decl_diff_number_11': len(var_decl_diff_lines_11),
            'super_method_call_number': len(super_m_lines),
            'for_type_cast_number': len(for_type_cast_lines),
            'this_find_number': len(this_lines),
            'asserts': len(asserts_lines),
            'setter': len(setter_lines),
            'empty_rethrow': len(empty_rethrow_lines),
            'prohibited_class_names': len(prohibited_class_names),
            'if_return': len(if_return_lines),
            'impl_multi': len(impl_multi_lines),
            'many_prim_ctors': len(many_prim_ctors_lines),
            'multiple_try': len(multiple_try_lines),
            'non_final_field': len(non_final_field_lines),
            'null_check': len(null_check_lines),
            'part_sync': len(part_sync_lines),
            'red_catch': len(red_catch_lines),
            'return_null': len(return_null_lines),
            # lines info about feature location
            'lines_instance_of_number': instance_of_lines,
            'lines_this_find': this_lines,
            'lines_method_chain_number': method_chain_lines,
            'lines_var_decl_diff_5': var_decl_diff_lines_5,
            'lines_var_decl_diff_7': var_decl_diff_lines_7,
            'lines_var_decl_diff_11': var_decl_diff_lines_11,
            'lines_super_method_call_number': super_m_lines,
            'lines_for_type_cast_number': for_type_cast_lines,
            'lines_string_concat': concat_str_number,
            'lines_for_var_middle': var_numbers,
            'lines_for_cycle': nested_for_blocks,
            'lines_for_if': nested_if_blocks,
            'lines_for_asserts': len(asserts_lines),
            'lines_for_setter': len(setter_lines),
            'lines_for_empty_rethrow': len(empty_rethrow_lines),
            'lines_for_prohibited_class_names': len(prohibited_class_names),
            'lines_for_if_return': len(if_return_lines),
            'lines_for_impl_multi': len(impl_multi_lines),
            'lines_for_many_prim_ctors': len(many_prim_ctors_lines),
            'lines_for_multiple_try': len(multiple_try_lines),
            'lines_for_non_final_field': len(non_final_field_lines),
            'lines_for_null_check': len(null_check_lines),
            'lines_for_part_sync': len(part_sync_lines),
            'lines_for_red_catch': len(red_catch_lines),
            'lines_for_return_null': len(return_null_lines),
            # some numerical characteristics
            'entropy': entropy,
            'left_spaces_var': left_space_variance,
            'right_spaces_var': right_space_variance,
            'max_left_diff_spaces': max_left_space_diff,
            'max_right_diff_spaces': max_right_space_diff,
            'ncss_lightweight': ncss_lightweight,
        }
    except Exception:
        # exc_type, exc_value, exc_tb = sys.exc_info()
        exceptions[file_local_dir] = traceback.format_exc()


if __name__ == '__main__':
    start = time.time()

    path = 'target/04'
    os.makedirs(path, exist_ok=True)
    filename = Path(path, '04-find-patterns.csv')
    fields = [
        'filename',
        # lines number
        'var_middle_number',
        'nested_for_number',
        'nested_if_number',
        'string_concat_number',
        'instance_of_number',
        'method_chain_number',
        'var_decl_diff_number_5',
        'var_decl_diff_number_7',
        'var_decl_diff_number_11',
        'super_method_call_number',
        'for_type_cast_number',
        'this_find_number',
        'asserts',
        'setter',
        'empty_rethrow',
        'prohibited_class_names',
        'if_return',
        'impl_multi',
        'many_prim_ctors',
        'multiple_try',
        'non_final_field',
        'null_check',
        'part_sync',
        'red_catch',
        'return_null',
        # lines info about feature location
        'lines_instance_of_number',
        'lines_this_find',
        'lines_method_chain_number',
        'lines_var_decl_diff_5',
        'lines_var_decl_diff_7',
        'lines_var_decl_diff_11',
        'lines_super_method_call_number',
        'lines_for_type_cast_number',
        'lines_string_concat',
        'lines_for_var_middle',
        'lines_for_cycle',
        'lines_for_if',
        'lines_for_asserts',
        'lines_for_setter',
        'lines_for_empty_rethrow',
        'lines_for_prohibited_class_names',
        'lines_for_if_return',
        'lines_for_impl_multi',
        'lines_for_many_prim_ctors',
        'lines_for_multiple_try',
        'lines_for_non_final_field',
        'lines_for_null_check',
        'lines_for_part_sync',
        'lines_for_red_catch',
        'lines_for_return_null',
        # some numerical characteristics
        'entropy',
        'left_spaces_var',
        'right_spaces_var',
        'max_left_diff_spaces',
        'max_right_diff_spaces',
        'ncss_lightweight'
    ]
    with open(filename, 'w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(
            csv_file, delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            fieldnames=fields)
        writer.writeheader()

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    log_func = partial(log_result, file_to_write=str(filename))
    manager = Manager()
    exceptions = manager.dict()
    func = partial(execute_python_code_in_parallel_thread, exceptions)
    with open(args.filename, 'r') as f:
        file_names = [i for i in f.readlines()]
    with open(filename, 'a', newline='\n', encoding='utf-8') as csv_file:
        for result in pool.imap(func, file_names):
            try:
                if result:
                    writer = csv.DictWriter(
                        csv_file, delimiter=';',
                        quotechar='"',
                        quoting=csv.QUOTE_MINIMAL,
                        fieldnames=fields)
                    writer.writerow(result)
                    csv_file.flush()
            except Exception:
                print('Writing to {} has failed'.format(filename))
                continue

    pool.close()
    pool.join()

    end = time.time()
    print('It took {} seconds'.format(str(end - start)))

    errors_log_path = str(Path(dir_path, 'errors.csv')).strip()
    if exceptions:
        with open(errors_log_path, 'w', newline='') as myfile:
            writer = csv.writer(myfile)
            for key, value in dict(exceptions).items():
                writer.writerow([key, value])
            # for ex in list(exceptions):
            #     wr.writerow(ex)
