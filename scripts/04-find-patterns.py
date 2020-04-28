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
import subprocess
import sys
import time
import traceback
from collections import defaultdict
from functools import partial
from multiprocessing import Manager
from pathlib import Path
from shutil import copyfile, rmtree

from aibolit.config import CONFIG

parser = argparse.ArgumentParser(description='Find patterns in Java files')
parser.add_argument(
    '--filename',
    help='path for file with a list of Java files',
    required=True)

args = parser.parse_args()
dir_path = os.path.dirname(os.path.realpath(__file__))
MI_pipeline_exclude_codes = [
    "M5",  # metric not ready
    "P27",  # empty implementation
]


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

    file = str(Path(dir_path, file_local_dir)).strip()
    p = Path(file)
    d_path = Path(os.environ['JAVA_FILES_PATH'] or dir_path)
    relative_path = p.relative_to(d_path)

    row = {'filename': p.as_posix()}
    for pattern in CONFIG['patterns']:
        val = None
        acronym = pattern['code']
        if acronym not in MI_pipeline_exclude_codes:
            try:
                val = pattern['make']().value(file)
                row[acronym] = len(val)
                row['lines_' + acronym] = val
            except Exception:
                row['lines_' + acronym] = row[acronym] = val
                exc_type, exc_value, exc_tb = sys.exc_info()
                row['lines_' + acronym] = row[acronym] = val
                traceback_str = traceback.format_exc()
                exceptions[file_local_dir] = {
                    'traceback': traceback_str,
                    'exc_type': str(exc_value),
                    'pattern_name': pattern['name'],
                }

    for metric in CONFIG['metrics']:
        val = None
        acronym = metric['code']
        if acronym not in MI_pipeline_exclude_codes:
            try:
                val = metric['make']().value(file)
                row[acronym] = val
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                row[acronym] = val
                traceback_str = traceback.format_exc()
                exceptions[file_local_dir] = {
                    'traceback': traceback_str,
                    'exc_type': str(exc_value),
                    'pattern_name': metric['name'],
                }
    return row


# flake8: noqa: C901
def write_log_error(exceptions):
    errors_log_path = str(Path(dir_path, 'errors.csv')).strip()
    exp_sorter = defaultdict(set)
    exp_number = defaultdict(int)
    if exceptions:
        # Write all traceback
        exc_dict = dict(exceptions)
        with open(errors_log_path, 'w', newline='') as myfile:
            writer = csv.writer(myfile)
            for filename, ex in exc_dict.items():
                writer.writerow([filename, ex['traceback']])
                exp_sorter[ex['pattern_name']].add(ex['exc_type'])
                exp_number[ex['pattern_name']] += 1

        dir_log_to_create = Path(dir_path, 'log')
        if not dir_log_to_create.exists():
            dir_log_to_create.mkdir(parents=True)

        exceptions_number_path = str(Path(dir_path, 'log/exceptions_number.csv')).strip()
        exceptions_unique_path = str(Path(dir_path, 'log/exceptions_unique.csv')).strip()

        with open(exceptions_unique_path, 'w', newline='') as myfile:
            writer = csv.writer(myfile)
            for pattern, exceptions in dict(exp_sorter).items():
                writer.writerow([pattern] + list(exceptions))

        with open(exceptions_number_path, 'w', newline='') as myfile:
            writer = csv.writer(myfile)
            for pattern, number in dict(exp_number).items():
                writer.writerow([pattern, number])

        filenames_w_errs = list(exc_dict.keys())
        dir_to_create = Path(dir_path, 'log/files')
        if not dir_to_create.exists():
            dir_to_create.mkdir(parents=True)
        files_with_errors = str(Path(dir_path, 'log/files/files_with_exceptions.txt')).strip()

        with open(files_with_errors, 'w') as myfile:
            myfile.writelines(filenames_w_errs)

        copied_files = []
        for i in filenames_w_errs:
            file = i.strip()
            src_path = Path(file)
            if src_path.exists():
                dst_path = str(Path(dir_to_create, src_path.name))
                copyfile(str(src_path), dst_path)
                copied_files.append(dst_path)
                print(src_path, dst_path)

        if copied_files:
            try:
                tar_filename = str(Path(dir_path, 'log/files.tar.gz'))
                cmd = ['tar', '-czvf', tar_filename, str(dir_to_create.absolute())]
                output = subprocess.check_output(cmd).decode("utf-8").strip()
                print(output)
                rmtree(dir_to_create)
                print('Path {} deleted with all files inside'.format(str(dir_to_create)))
            except Exception:
                print(f"E: {traceback.format_exc()}")


if __name__ == '__main__':
    start = time.time()

    path = 'target/04'
    os.makedirs(path, exist_ok=True)
    filename = Path(path, '04-find-patterns.csv')
    fields = \
        [x['code'] for x in CONFIG['patterns'] if x['code'] not in MI_pipeline_exclude_codes] \
        + [x['code'] for x in CONFIG['metrics'] if x['code'] not in MI_pipeline_exclude_codes] \
        + ['lines_' + x['code'] for x in CONFIG['patterns'] if x['code'] not in MI_pipeline_exclude_codes] \
        + ['filename']

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
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, file=sys.stdout)
                continue

    pool.close()
    pool.join()

    end = time.time()
    print('It took {} seconds'.format(str(end - start)))

    write_log_error(exceptions)
