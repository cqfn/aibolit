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
import os
import queue as queue
from pathlib import Path

# from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.var_middle.var_middle import VarMiddle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find the pattern which has the largest impact on readability'
    )
    parser.add_argument(
        '--filename',
        help='path for Java file',
        required=True)

    args = parser.parse_args()
    cur_file_dir = Path(os.path.realpath(__file__)).parent
    java_file = str(Path(cur_file_dir, args.filename))

    order_queue = queue.Queue()
    # concat_result = StringConcatFinder().value(java_file)
    depth_for = 2
    depth_if = 2
    for_result = NestedBlocks(depth_for, block_type=BlockType.FOR).value(java_file)
    if_result = NestedBlocks(depth_if, block_type=BlockType.IF).value(java_file)
    var_middle_result = VarMiddle().value(java_file)

    if var_middle_result:
        order_queue.put([var_middle_result, 'variable declaration in the middle of the function'])
    if for_result:
        order_queue.put([for_result, 'nested for cycle with depth = {}'.format(depth_for)])
    if if_result:
        order_queue.put([if_result, 'nested if condition with depth = 2'.format(depth_if)])

    # if concat_result:
    #     order_queue.put([concat_result, 'string concatenation with operator +'])

    lines, output_string = order_queue.get()
    for line in lines:
        if line:
            print('Line {}. Low readability due to: {}'.format(
                line,
                output_string
            ))
    order_queue.task_done()
