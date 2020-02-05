from pathlib import Path
import argparse
import aiofiles
import asyncio
from subprocess import Popen, PIPE
import multiprocessing
import subprocess
import shlex
import time
from multiprocessing import Process
from multiprocessing.pool import ThreadPool, Pool
from multiprocessing import Pool
from subprocess import call
import os

parser = argparse.ArgumentParser(description='Compute Readability score')
parser.add_argument('--filename',
                    help='path for file with a list of Java files')

args = parser.parse_args()
dir_path = os.path.dirname(os.path.realpath(__file__))
results = []


def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    results.append(result)


def call_proc(cmd):
    """ This runs in a separate thread. """
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out


# p = subprocess.Popen(
#     ['java', '-jar', jar_path, file_path],
#     shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# p = subprocess.Popen(
#     ['timeout', '4', '/nobreak'],
#     shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


# pool.apply_async(call_proc, args=(['timeout', '4', '/nobreak'],), callback=log_result)
# p = subprocess.Popen(
#     ['java', '-jar',
#      'D:\\PycharmProjects\\readbility\\01\\repos\\Algorithms\\src\\main\\java\\com\\williamfiset\\algorithms\\datastructures\\linkedlist\\DoublyLinkedList.java',
#      'D:\\PycharmProjects\\readbility\\aibolit\\aibolit\\scripts\\readbility.jar'],
#     shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# print(p.stdout.readlines())


# async def run():
#     tasks = []
#     task = asyncio.ensure_future(open_file(args.filename))
#     tasks.append(task)
#     contents = await asyncio.gather(*tasks)
#     return contents

if __name__ == '__main__':
    t1 = time.time()
    pool = Pool(multiprocessing.cpu_count())
    jar_path = str(Path(dir_path, r'readability.jar')).strip()
    handled_files = []

    with open(args.filename, 'r') as f:
        for i in f.readlines():
            java_file = str(Path(dir_path, i)).strip()
            pool.apply_async(call_proc, args=(['ping', '127.0.0.1', '-n', '2'],), callback=log_result)
            # pool.apply_async(
            #     call_proc,
            #     args=(['java', '-jar', jar_path, java_file],),
            #     callback=log_result)

    pool.close()
    pool.join()

    print(results)
    t2 = time.time()
    print('It took this many seconds ' + str(t2 - t1))

    results = []
    t1 = time.time()
    with open(args.filename, 'r') as f:
        for i in f.readlines():
            java_file = str(Path(dir_path, i)).strip()
            p = subprocess.Popen(['ping', '127.0.0.1', '-n', '2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            results.append(out)

    print(results)
    t2 = time.time()
    print('It took this many seconds ' + str(t2 - t1))
