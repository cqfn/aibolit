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


import pandas as pd
import os
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.var_middle.var_middle import VarMiddle


def format_f(e):
    return f'{e}-{e}'


FILEPATH_TO_READ = 'target/01/found-java-files.txt'
DIR_TO_CREATE = 'target/03'
FILE_TO_SAVE = 'patterns.csv'

current_location: str = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
pattern_for = NestedBlocks(2, BlockType.FOR)
pattern_if = NestedBlocks(2, BlockType.IF)
pattern_var_middle = VarMiddle()
data = []
with open(current_location + FILEPATH_TO_READ) as fp:
    for line in fp.readlines():
        filename = line.strip()
        var_middle = list(map(format_f, pattern_var_middle.value(filename)))
        nested_fors = list(map(format_f, pattern_for.value(filename)))
        nested_ifs = list(map(format_f, pattern_if.value(filename)))
        data += [(
            filename,
            ';'.join(nested_fors),
            ';'.join(nested_ifs),
            ';'.join(var_middle)
        )]
if not os.path.isdir(DIR_TO_CREATE):
    os.makedirs(DIR_TO_CREATE)
pd.DataFrame(data, columns=['filename', 'for2', 'if2', 'var_middle']).to_csv(
    current_location + '/' + DIR_TO_CREATE + '/' + FILE_TO_SAVE,
    index=False
)
