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
import itertools
import multiprocessing
import os
import sys
import time
import javalang
from enum import Enum
from pathlib import Path
import pandas as pd
import traceback
import cchardet as chardet

parser = argparse.ArgumentParser(description='Filter important java files')
parser.add_argument(
    '--dir',
    help='dir for Java files search',
    required=True
)
parser.add_argument(
    '--max_classes',
    type=lambda v: sys.maxsize if v == '' else int(v),
    required=False,
    default=None
)
args = parser.parse_args()
MAX_CLASSES = args.max_classes
print('MAX_CLASSES', MAX_CLASSES)
TXT_OUT = 'found-java-files.txt'
CSV_OUT = '02-java-files.csv'

DIR_TO_CREATE = 'target/02'
FILE_TO_SAVE = '02-java-files.csv'
current_location: str = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)


class ClassType(Enum):
    INTERFACE = 1
    ENUM = 2
    ABSTRACT_CLASS = 3
    TEST = 4
    JAVA_PARSE_ERROR = 5
    CLASS = 999


def get_class_type(filename: Path):
    with open(filename, 'rb') as f:
        msg = f.read()
        result = chardet.detect(msg)

    with open(filename, 'r', encoding=result['encoding']) as f:
        text = f.read()
        class_type = ClassType.CLASS
        try:
            tree = javalang.parse.parse(text)
            for _, node in tree:
                if type(node) == javalang.tree.InterfaceDeclaration:
                    class_type = ClassType.INTERFACE
                    break
                elif type(node) == javalang.tree.EnumDeclaration:
                    class_type = ClassType.ENUM
                    break
                elif type(node) == javalang.tree.ClassDeclaration:
                    if 'abstract' in node.modifiers:
                        class_type = ClassType.ABSTRACT_CLASS
                        break
                    elif 'Test' in node.name:
                        class_type = ClassType.TEST
                        break
                    else:
                        class_type = ClassType.CLASS
                        break
        except Exception:
            class_type = ClassType.JAVA_PARSE_ERROR
        return class_type


def worker(filename: Path):
    """
    Identify type of class
    :param filename: filename of Java class
    :return: tuple of java file path and it's type
    """
    results = []
    str_filename = str(filename)
    if str_filename.lower().endswith('.java'):
        if str_filename.lower().endswith('test.java') or \
                any([x.lower().find('test') > -1 for x in filename.parts]) or \
                str_filename.lower().find('package-info') > -1:
            class_type = ClassType.TEST
        else:
            try:
                class_type = get_class_type(filename)
            except Exception:
                print("Can't open file {}. Ignoring the file ...".format(str_filename))
                traceback.print_exc()
                class_type = ClassType.JAVA_PARSE_ERROR

        results = [filename.as_posix(), class_type.value]

    return results


def walk_in_parallel():
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        walk = os.walk(args.dir)
        fn_gen = itertools.chain.from_iterable(
            (Path(os.path.join(root, file))
             for file in files)
            for root, dirs, files in walk)

        results = pool.map(worker, fn_gen)

    top_n = MAX_CLASSES if MAX_CLASSES is not None else len(results)
    return [v for v in results if len(v) > 0][0: top_n]


if __name__ == '__main__':
    start = time.time()
    results = walk_in_parallel()

    if not os.path.isdir(DIR_TO_CREATE):
        os.makedirs(DIR_TO_CREATE)

    path_csv_out = str(Path(current_location, DIR_TO_CREATE, CSV_OUT))
    path_txt_out = str(Path(current_location, DIR_TO_CREATE, TXT_OUT))
    df = pd.DataFrame(results, columns=['filename', 'class_type'])
    df = df[df['class_type'] == 999]
    df.to_csv(path_csv_out, index=False)
    df['filename'].to_csv(path_txt_out, header=None, index=None)
    end = time.time()
    print('It took ' + str(end - start) + ' seconds')
