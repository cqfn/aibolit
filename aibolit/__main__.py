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
import queue as queue
import sys
from pathlib import Path

from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.patterns.var_middle.var_middle import VarMiddle
from aibolit import __version__


def main():
    exit_status = -1
    try:
        depth_for = 2
        depth_if = 2
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

            order_queue = queue.Queue()
            order_queue.put([
                VarMiddle().value(java_file),
                'variable declaration in the middle of the function'])
            order_queue.put([
                NestedBlocks(depth_for, block_type=BlockType.FOR).value(java_file),
                'nested for cycle with depth = {}'.format(depth_for)])
            order_queue.put([
                NestedBlocks(depth_if, block_type=BlockType.IF).value(java_file),
                'nested if condition with depth = 2'.format(depth_if)])
            order_queue.put([
                StringConcatFinder().value(java_file),
                'string concatenation with operator +'])

            lines, output_string = order_queue.get()
            if not lines:
                print('Your code is perfect in aibolit\'s opinion')
            for line in lines:
                if line:
                    print('Line {}. Low readability due to: {}'.format(
                        line,
                        output_string
                    ))
            order_queue.task_done()
            exit_status = 0
    except KeyboardInterrupt:
        exit_status = -1
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
