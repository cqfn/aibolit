import pandas as pd
import os
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.var_middle.var_middle import VarMiddle

def format_f(e):
    return f'{e}-{e}'


FILEPATH_TO_READ = '/01/found-java-files.txt'
DIR_TO_CREATE = '03'
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
pd.DataFrame(
    data, columns=['filename', 'for2', 'if2', 'var_middle']
).to_csv(
    current_location + '/' + DIR_TO_CREATE + '/' + FILE_TO_SAVE,
    index=False
)