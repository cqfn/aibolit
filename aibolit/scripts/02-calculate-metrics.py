import os
import sys
from filelock import FileLock
import threading

OUT_FILE_NAME = '02/file_metrics.csv'
THREADS_NUM = 6


def process_files(nthread, files):
    total = len(files)
    chunk = round(total / THREADS_NUM)
    m = total if chunk * (nthread + 1) > total else chunk * (nthread + 1)
    for i in range(chunk * nthread, m):
        process_file(files[i])


def process_file(file):
    print(file)
    try:
        sys.path.append('../')
        from metrics.cc.main import CCMetric
        from metrics.loc.loc import Loc
        from metrics.npath.main import NPathMetric
        m = CCMetric(file[:-1])
        cc = m.value(False)['data'][0]['complexity']
        m = Loc(file[:-1])
        loc = m.value()
        m = NPathMetric(file[:-1])
        npath = m.value(False)['data'][0]['complexity']
        lock_path = '{}.lock'.format(OUT_FILE_NAME)
        lock = FileLock(lock_path, timeout=10)
        with lock:
            open(OUT_FILE_NAME, 'a').write('{};{};{};{}\n'.format(file[:-1], cc, loc, npath))
    except Exception as e:
        print(file, str(e))


if __name__ == '__main__':
    with open('01/found-java-files.txt', 'r') as f:
        files = f.readlines()

    if not os.path.isdir('02'):
        os.makedirs('02')
    with open(OUT_FILE_NAME, 'w+') as f:
        f.write('file;cc;loc;npath')

    for i in range(THREADS_NUM):
        x = threading.Thread(target=process_files, args=(i, files))
        x.start()
