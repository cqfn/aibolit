# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT


import argparse
from dataclasses import dataclass, field
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from ctypes import c_bool
from enum import Enum
from functools import partial
from multiprocessing import Value, Manager, cpu_count, Lock
from multiprocessing.sharedctypes import Synchronized
from multiprocessing.synchronize import Lock as LockBase
from pathlib import Path

import chardet
import javalang
import javalang.tree
import pandas as pd
from sklearn.model_selection import train_test_split

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
    default=sys.maxsize
)
parser.add_argument(
    '--split_only',
    required=False,
    help='Only split filenames into train and test, do not filter',
    default=False,
    action='store_true'
)
args = parser.parse_args()
MAX_CLASSES = args.max_classes
TXT_OUT = 'found-java-files.txt'
CSV_OUT = '02-java-files.csv'
current_location: str = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
target_folder = os.getenv('TARGET_FOLDER')
if target_folder:
    Path(target_folder).mkdir(parents=True, exist_ok=True)
else:
    target_folder = str(Path(current_location).absolute())

print(f'Target folder: {target_folder}')
DIR_TO_CREATE = Path(target_folder, 'target/02')
FILE_TO_SAVE = '02-java-files.csv'


class ClassType(Enum):
    INTERFACE = 1
    ENUM = 2
    ABSTRACT_CLASS = 3
    TEST = 4
    JAVA_PARSE_ERROR = 5
    NESTED_CLASSES = 6
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
            classes = list(tree.filter(javalang.tree.ClassDeclaration))
            if len(classes) > 1:
                class_type = ClassType.NESTED_CLASSES
            else:
                for _, node in tree:
                    if isinstance(node, javalang.tree.InterfaceDeclaration):
                        class_type = ClassType.INTERFACE
                        break
                    elif isinstance(node, javalang.tree.EnumDeclaration):
                        class_type = ClassType.ENUM
                        break
                    elif isinstance(node, javalang.tree.ClassDeclaration):
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


def worker(queue, counter):
    """
    Identify type of class

    :return: tuple of java file path and it's type
    """
    result_item = []
    if not queue.empty():
        filename = queue.get()
        str_filename = str(filename)
        if str_filename.lower().endswith('.java'):
            if str_filename.lower().endswith('test.java') or \
                    any(x.lower().find('test') > -1 for x in filename.parts) or \
                    str_filename.lower().find('package-info') > -1:
                class_type = ClassType.TEST
            else:
                try:
                    class_type = get_class_type(filename)
                except Exception:
                    print(f"Can't open file {str_filename}. Ignoring the file ...")
                    traceback.print_exc()
                    class_type = ClassType.JAVA_PARSE_ERROR

            result_item = [filename.as_posix(), class_type.value]

        if result_item:
            if result_item[1] == 999:
                counter.increment()

    return result_item


def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            if entry.name.endswith('.java') and entry.is_file():
                yield entry.path


@dataclass(slots=True)
class SharedCounter:
    val: Synchronized
    lock: LockBase = field(default_factory=Lock)

    def increment(self):
        with self.lock:
            self.val.value += 1

    @property
    def value(self):
        return self.val.value


class Counter:
    def __init__(self, initval=0):
        self._initval = initval

    def shared(self):
        return SharedCounter(val=Value('i', self._initval))


def walk_in_parallel():
    manager = Manager()
    queue = manager.Queue()

    for i in scantree(args.dir):
        queue.put(Path(i).absolute())

    cancel = Value(c_bool, False)

    def call_back():
        if counter.value > MAX_CLASSES:
            cancel.value = True
            try:
                while True:
                    queue.get_nowait()
            except Exception:
                pass

    collected_results = []

    counter = Counter(1).shared()
    p = ThreadPoolExecutor(cpu_count())

    while not cancel.value and not queue.empty():
        call_back()
        f = partial(worker, queue)
        collected_results.append(p.submit(f, counter).result())

    return [v for v in collected_results if len(v) > 0]


if __name__ == '__main__':
    path_csv_out = str(Path(DIR_TO_CREATE, CSV_OUT))
    path_txt_out = str(Path(DIR_TO_CREATE, TXT_OUT))

    if not args.split_only:
        start = time.time()
        results = walk_in_parallel()

        if not os.path.isdir(DIR_TO_CREATE):
            os.makedirs(DIR_TO_CREATE)

        df = pd.DataFrame(results, columns=['filename', 'class_type'])
        df = df[df['class_type'] == 999]
        df.to_csv(path_csv_out, index=False)
        df['filename'].to_csv(path_txt_out, header=None, index=None, encoding='utf-8')
        end = time.time()
        print('It took ' + str(end - start) + ' seconds')
    df = pd.read_csv(path_csv_out)
    train, test = train_test_split(df['filename'], test_size=0.3, random_state=42)
    train_csv_file = str(Path(DIR_TO_CREATE, '02-train.csv'))
    test_csv_file = str(Path(DIR_TO_CREATE, '02-test.csv'))
    train.to_csv(train_csv_file, index=False)
    test.to_csv(test_csv_file, index=False)
