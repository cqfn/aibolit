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
import sys
from pathlib import Path

from aibolit import __version__
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.string_concat.string_concat import StringConcatFinder
from aibolit.patterns.var_middle.var_middle import VarMiddle
import argparse
import multiprocessing
import os
import subprocess
import time
from multiprocessing import Pool
from pathlib import Path
import csv
import sys


def find_halstead(java_file):
    halstead_dir = str(Path(Path(os.getcwd()).parent, r'aibolit\scripts\halstead.jar'))
    cmd = ['java', '-jar', halstead_dir, java_file]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    score = None
    if not err:
        score = float(out.decode().split('readability:')[-1].strip())
    else:
        print('Error when running: {}'.format(err))
    return score


def find_ncss(java_file):
    return 0


def predict(halstead_volume, ncss):
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
            ncss_value = find_halstead(java_file)
            order_queue = predict(halstead_volume, ncss_value)
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
