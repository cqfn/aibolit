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
from aibolit.config import Config
import pandas as pd

current_location: str = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)
target_folder = os.getenv('TARGET_FOLDER')
if target_folder:
    os.chdir(target_folder)
else:
    target_folder = os.path.dirname(os.path.realpath(__file__))


def log_result(result, file_to_write):
    """ Save result to csv file. """
    with open(file_to_write, 'a', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(
            csv_file, delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            fieldnames=list(result.keys()))
        writer.writerow(result)


def execute_python_code_in_parallel_thread(exceptions, features_to_extract, file_absolute_path):
    """ This runs in a separate thread. """

    file_absolute_path = file_absolute_path.strip()
    file_path = Path(file_absolute_path)
    row = {'filename': file_path.absolute().as_posix()}

    if features_to_extract:
        config = {}
        config['patterns'] = [x for x in config['patterns'] if x['code'] in features_to_extract]
        config['metrics'] = [x for x in config['metrics'] if x['code'] in features_to_extract]
    else:
        config = Config.get_patterns_config()

    for pattern in config['patterns']:
        val = None
        acronym = pattern['code']
        if acronym not in config['patterns_exclude']:
            try:
                val = pattern['make']().value(str(file_path))
                row[acronym] = len(val)
                row['lines_' + acronym] = val
            except Exception:
                row['lines_' + acronym] = row[acronym] = val
                exc_type, exc_value, exc_tb = sys.exc_info()
                row['lines_' + acronym] = row[acronym] = val
                traceback_str = traceback.format_exc()
                exceptions[file_absolute_path] = {
                    'traceback': traceback_str,
                    'exc_type': str(exc_value),
                    'pattern_name': pattern['name'],
                }

    for metric in config['metrics']:
        val = None
        acronym = metric['code']
        if acronym not in config['metrics_exclude']:
            try:
                val = metric['make']().value(str(file_path))
                row[acronym] = val
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                row[acronym] = val
                traceback_str = traceback.format_exc()
                exceptions[file_absolute_path] = {
                    'traceback': traceback_str,
                    'exc_type': str(exc_value),
                    'pattern_name': metric['name'],
                }
    return row


# flake8: noqa: C901
def write_log_error(exceptions):
    errors_log_path = str(Path(target_folder, 'errors.csv')).strip()
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

        dir_log_to_create = Path(target_folder, 'log')
        if not dir_log_to_create.exists():
            dir_log_to_create.mkdir(parents=True)

        exceptions_number_path = str(Path(target_folder, 'log/exceptions_number.csv')).strip()
        exceptions_unique_path = str(Path(target_folder, 'log/exceptions_unique.csv')).strip()

        with open(exceptions_unique_path, 'w', newline='') as myfile:
            writer = csv.writer(myfile)
            for pattern, exceptions in dict(exp_sorter).items():
                writer.writerow([pattern] + list(exceptions))

        with open(exceptions_number_path, 'w', newline='') as myfile:
            writer = csv.writer(myfile)
            for pattern, number in dict(exp_number).items():
                writer.writerow([pattern, number])

        filenames_w_errs = list(exc_dict.keys())
        dir_to_create = Path(target_folder, 'log/files')
        if not dir_to_create.exists():
            dir_to_create.mkdir(parents=True)
        files_with_errors = str(Path(target_folder, 'log/files/files_with_exceptions.txt')).strip()

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
                tar_filename = str(Path(target_folder, 'log/files.tar.gz'))
                cmd = ['tar', '-czvf', tar_filename, str(dir_to_create.absolute())]
                output = subprocess.check_output(cmd).decode("utf-8").strip()
                print(output)
                rmtree(dir_to_create)
                print('Path {} deleted with all files inside'.format(str(dir_to_create)))
            except Exception:
                print(f"E: {traceback.format_exc()}")


def run_dataset_calculation(file_names, features_to_extract=None):
    start = time.time()

    path = 'target/04'
    os.makedirs(path, exist_ok=True)
    filename = Path(path, '04-find-patterns.csv')
    config = Config.get_patterns_config()
    patterns_exclude = config['patterns_exclude']
    fields = \
        [x['code'] for x in config['patterns'] if x['code'] not in patterns_exclude] \
        + [x['code'] for x in config['metrics'] if x['code'] not in config['metrics_exclude']] \
        + ['lines_' + x['code'] for x in config['patterns'] if x['code'] not in patterns_exclude] \
        + ['filename']

    with open(filename, 'w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(
            csv_file, delimiter=';',
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            fieldnames=fields)
        writer.writeheader()

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    manager = Manager()
    exceptions = manager.dict()
    func = partial(execute_python_code_in_parallel_thread, features_to_extract, exceptions)
    sep = ';'
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
    return pd.read_csv(filename, sep=sep)
