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

# You need to download the archive here:
# https://dibt.unimol.it/report/readability/files/readability.zip
# Unzip and put it into the executable's current directory

parser = argparse.ArgumentParser(description='Compute Readability score')
parser.add_argument('--filename',
                    help='path for file with a list of Java files',
                    required=True)

args = parser.parse_args()

dir_path = os.path.dirname(os.path.realpath(__file__))
target_folder = Path(os.getenv('TARGET_FOLDER'))
if target_folder:
    os.chdir(str(target_folder))

results = {}
path = 'target/05'
os.makedirs(path, exist_ok=True)
csv_file = open('target/05/05_readability.csv', 'w', newline='\n', encoding='utf-8')
writer = csv.writer(
    csv_file, delimiter=';',
    quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['filename', 'readability'])


def log_result(result):
    """ Save result to csv file. """
    writer.writerow(result)
    csv_file.flush()


def call_proc(cmd, file_path):
    """ This runs in a separate thread. """
    print('Running ', ' '.join(cmd))
    p = subprocess.Popen(
        cmd,
        cwd=os.path.dirname(os.path.realpath(__file__)) + '/_tmp',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    score = None
    if not err:
        score = float(out.decode().rsplit('readability:', maxsplit=1)[-1].strip())
    else:
        print(f'Error when running: {err}')
    return file_path.strip(), score


if __name__ == '__main__':
    t1 = time.time()
    pool = Pool(multiprocessing.cpu_count())
    handled_files = []

    with open(args.filename, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            java_file = str(Path(dir_path, i)).strip()
            pool.apply_async(
                call_proc,
                args=(['java', '-jar', 'rsm.jar', java_file], i,),
                callback=log_result)

    pool.close()
    pool.join()

    print(results)
    t2 = time.time()
    print('It took this many seconds ' + str(t2 - t1))
