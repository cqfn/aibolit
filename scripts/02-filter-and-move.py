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
import time
import javalang
from enum import Enum
import csv
import shutil
from pathlib import Path
import sys
from functools import partial
import pandas as pd

parser = argparse.ArgumentParser(description='Filter important java files')
parser.add_argument(
    '--dir',
    help='dir for Java files search',
    required=True)
parser.add_argument('--max_classes', type=int, required=False, default=sys.maxsize)
results = []
args = parser.parse_args()
dir_path = Path(os.path.dirname(os.path.realpath(__file__))).absolute()
files_list = []


class ClassType(Enum):
    INTERFACE = 1
    ENUM = 2
    ABSTRACT_CLASS = 3
    TEST = 4
    JAVA_PARSE_ERROR = 5
    CLASS = 999


def get_class_type(filename):
    with open(filename, 'r', encoding='utf-8') as f:
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


def worker(filename, target_path):
    """
    Idetify type of class
    :param filename: filename of Java class
    :return: tuple of java file path and it's type
    """
    global results
    if filename.lower().endswith('.java'):
        if filename.lower().endswith('test.java'):
            class_type = ClassType.TEST
            z = Path(filename).as_posix()
            # if not z:
            #     print(filename)
            # writer.writerow([Path(filename).as_posix(), class_type.value])
            results.append([Path(filename).as_posix(), class_type.value])
            # csv_file.flush()
        else:
            class_type = get_class_type(filename)
            from_path = Path(filename).absolute()
            d_path = Path(dir_path)
            filename_posix = from_path.relative_to(d_path)
            # if not filename_posix:
            #     print(filename)
            java_filename_posix = str(Path(filename).as_posix())
            temp_local_path = java_filename_posix.replace(args.dir + '/', '')
            to_path = Path(dir_path, target_path, temp_local_path)
            if class_type in [ClassType.CLASS, ClassType.JAVA_PARSE_ERROR]:
                if not to_path.parent.exists():
                    os.makedirs(to_path.parent)
                if not to_path.exists():
                    shutil.copy(from_path, to_path)
            results.append([Path(filename).as_posix(), class_type.value])


def walk_in_parallel():
    target_path = 'target/02'
    csv_output_file = target_path + '/02-java-files.csv'
    os.makedirs(target_path, exist_ok=True)
    with open(csv_output_file, 'w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(
            csv_file,
            delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['filename', 'class_type'])

    with multiprocessing.Pool(20) as pool:
        walk = os.walk(args.dir)
        fn_gen = itertools.chain.from_iterable(
            (os.path.join(root, file)
             for file in files)
            for root, dirs, files in walk)

        func = partial(worker, target_path=target_path)
        pool.map(func, fn_gen)


if __name__ == '__main__':
    start = time.time()
    walk_in_parallel()

    for result in results:
        with open('target/02-java-files.csv', 'a', newline='\n', encoding='utf-8') as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL)

            writer.writerow([filename_posix.as_posix(), class_type.value])

    df = pd.read_csv('target/02/02-java-files.csv', sep=';')
    df['filename'].to_csv('target/02/found-java-files.txt', header=None, index=None)

    end = time.time()
    print('It took ' + str(end - start) + ' seconds')
