import argparse
import multiprocessing
import os
import subprocess
import time
from multiprocessing import Pool
from pathlib import Path
import csv
from var_middle import VarMiddle
from nested_blocks import NestedBlocks

# You need to download the archive here:
# https://dibt.unimol.it/report/readability/files/readability.zip
# Unzip and put it into the executable's current directory

parser = argparse.ArgumentParser(description='Compute Readability score')
parser.add_argument('--filename',
                    help='path for file with a list of Java files',
                    required=True)

args = parser.parse_args()

dir_path = os.path.dirname(os.path.realpath(__file__))

path = '05'
os.makedirs(path, exist_ok=True)
csv_file = open('05/05_run_var.csv', 'w', newline='\n')
writer = csv.writer(
    csv_file, delimiter=';',
    quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['filename', 'var_middle_number', 'nested_double_for_number'])

def log_result(result):
    """ Save result to csv file. """
    #print(len(result[1]))
    writer.writerow([result[0], len(result[1]), len(result[2])])
    csv_file.flush()

def run_VarMiddle(java_file):
    """ This runs in a separate thread. """
    #print(java_file)
    lines = VarMiddle().value(java_file)
    #print(1)
    nested_blocks = NestedBlocks(2).value(java_file)
    #print(6)
    #lines = pattern.value(java_file)
    #print('Variables are declared in the middle there: {}'.format(lines))
    return java_file, lines, nested_blocks


if __name__ == '__main__':
    t1 = time.time()
    pool = Pool(multiprocessing.cpu_count())
    handled_files = []

    with open(args.filename, 'r') as f:
        for i in f.readlines():
            java_file = str(Path(dir_path, i)).strip()
            pool.apply_async(
                run_VarMiddle,
                args=(java_file,),
                callback=log_result)
                
    pool.close()
    pool.join()

    t2 = time.time()
    print('It took this many seconds ' + str(t2 - t1))
