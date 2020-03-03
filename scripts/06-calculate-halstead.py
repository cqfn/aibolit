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
results = {}

path = 'target/06'
os.makedirs(path, exist_ok=True)
csv_file = open(path + '/06_halstead_volume.csv', 'w', newline='\n')
writer = csv.writer(csv_file,
                    delimiter=';',
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
writer.writerow(['filename', 'halstead volume'])


def log_result(result):
    """ Save result to csv file. """
    writer.writerow(result)
    csv_file.flush()


def call_proc(cmd, java_file):
    """ This runs in a separate thread. """
    print('Running ', ' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    score = None
    if not err:
        score = float(out.decode().split('readability:')[-1].strip())
    else:
        print('Error when running: {}'.format(err))
    return java_file.strip(), score


if __name__ == '__main__':
    t1 = time.time()
    pool = Pool(multiprocessing.cpu_count())
    handled_files = []
    count = 0

    with open(args.filename, 'r') as f:
        for i in f.readlines():
            if count < args.max_count:
                java_file = str(Path(dir_path, i)).strip()
                pool.apply_async(
                    call_proc,
                    args=(
                        ['java', '-jar', 'halstead.jar', java_file],
                        i,
                    ),
                    callback=log_result)
                count += 1
            else:
                break

    pool.close()
    pool.join()

    print(results)
    t2 = time.time()
    print('It took this many seconds ' + str(t2 - t1))
