# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT


import argparse
import multiprocessing
import os
import subprocess
import time
from multiprocessing import Pool
from pathlib import Path
import csv
import sys

# You need to run `mvn clean` in metrics/halsteadvolume.
# You will to get a jar file  in `target` directory.
# Rename it to halstead.jar and put it into the executable's
# current directory

parser = argparse.ArgumentParser(description='Compute Readability score')
parser.add_argument('--filename',
                    help='path for file with a list of Java files',
                    required=True)
parser.add_argument('--max_count',
                    help='max number of files for analyzing',
                    default=sys.maxsize,
                    nargs='?',
                    type=int)

args = parser.parse_args()

dir_path = os.path.dirname(os.path.realpath(__file__))
target_folder = Path(os.getenv('TARGET_FOLDER'))
results = {}

path = 'target/06'
os.makedirs(path, exist_ok=True)
csv_file = open(path + '/06_halstead_volume.csv', 'w', newline='\n', encoding='utf-8')
writer = csv.writer(
    csv_file, delimiter=';',
    quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['filename', 'halstead volume'])


def log_result(result):
    """ Save result to csv file. """
    writer.writerow(result)
    csv_file.flush()


def call_proc(cmd, file_path):
    """ This runs in a separate thread. """
    print('Running ', ' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    score = None
    if not err:
        score = float(out.decode().rsplit('readability:', maxsplit=1)[-1].strip())
    else:
        print(f'Error when running: {err}')
    return str(Path(file_path.strip()).absolute()), score


if __name__ == '__main__':
    t1 = time.time()
    pool = Pool(multiprocessing.cpu_count())
    handled_files = []
    count = 0
    max_count = args.max_count
    halstead_location = str(Path(dir_path, 'halstead.jar'))
    print(f'halstead location: {halstead_location}')
    print(max_count)
    with open(args.filename, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            if count < max_count:
                java_file = str(Path(dir_path, i)).strip()
                pool.apply_async(
                    call_proc,
                    args=(['java', '-jar', halstead_location, java_file], i,),
                    callback=log_result)
                count += 1
            else:
                break

    pool.close()
    pool.join()

    print(results)
    t2 = time.time()
    print('It took this many seconds ' + str(t2 - t1))
