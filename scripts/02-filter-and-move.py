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


parser = argparse.ArgumentParser(description='Filter important java files')
parser.add_argument(
    '--dir',
    help='dir for Java files search',
    required=True)
parser.add_argument('--max-classes', type=int, required=False, default=sys.maxsize)
args = parser.parse_args()
dir_path = os.path.dirname(os.path.realpath(__file__))
files_list = []
path = '02'
os.makedirs(path, exist_ok=True)
csv_file = open('target/01/found-java-files.txt', 'w', newline='\n')
debug_log = open('debug.txt', 'w')
max_classes = args.max_classes

writer = csv.writer(
    csv_file,
    delimiter=';',
    quotechar='"',
    quoting=csv.QUOTE_MINIMAL)


class ClassType(Enum):
    INTERFACE = 1
    ENUM = 2
    ABSTRACT_CLASS = 3
    TEST = 4
    JAVA_PARSE_ERROR = 5
    CLASS = 999


counter = 0
javaCounter = 81889


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
                    # debug_log.write(filename + ':  {}\n'.format(node.name))
                    # debug_log.flush()
                    # print(node.name, 'Test' in node.name)
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


def worker(filename):
    """
    Idetify type of class
    :param filename: filename of Java class
    :return: tuple of java file path and it's type
    """
    global javaCounter, counter
    print(str(counter / float(javaCounter)))
    if counter > max_classes:
        return
    if filename.lower().endswith('.java'):
        if filename.lower().endswith('test.java'):
            class_type = ClassType.TEST
            writer.writerow([filename, class_type.value])
            csv_file.flush()
        else:
            class_type = get_class_type(filename)
            if class_type in [ClassType.CLASS, ClassType.JAVA_PARSE_ERROR]:
                p = Path(filename)
                d_path = Path(dir_path)
                ltd = p.relative_to(d_path)
                debug_log.write('Path' + str(p) + 'd_path' + str(d_path) + 'ltd' + str(ltd) + '\n')
                debug_log.flush()
                new_path = Path('filtered_files', ltd)
                os.makedirs(new_path.parent, exist_ok=True)
                shutil.copy(filename, new_path)

            writer.writerow([filename, class_type.value])
            csv_file.flush()
            counter += 1


def walk_in_parallel():
    # print(1)
    print('Number of java files :' + str(javaCounter))
    with multiprocessing.Pool(1) as pool:
        walk = os.walk(args.dir)
        # print(list(os.walk(args.dir)))
        fn_gen = itertools.chain.from_iterable(
            (os.path.join(root, file)
             for file in files)
            for root, dirs, files in walk)

        pool.map(worker, fn_gen)


if __name__ == '__main__':
    t1 = time.time()
    walk_in_parallel()
    # print(worker(args.dir))
    t2 = time.time()
    print('It took ' + str(t2 - t1) + ' seconds ')
