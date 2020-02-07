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


import os
import sys
from filelock import FileLock
import threading

OUT_FILE_NAME = 'target/02/file-metrics.csv'
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
        from metrics.hv.main import HVMetric
        m = CCMetric(file[:-1])
        cc = m.value(False)['data'][0]['complexity']
        m = Loc(file[:-1])
        loc = m.value()
        m = NPathMetric(file[:-1])
        npath = m.value(False)['data'][0]['complexity']
        m = HVMetric(file[:-1])
        hv = m.value()['data'][0]['halsteadvolume']
        lock_path = '{}.lock'.format(OUT_FILE_NAME)
        lock = FileLock(lock_path, timeout=10)
        with lock:
            open(OUT_FILE_NAME, 'a').write('{};{};{};{};{}\n'.format(file[:-1], cc, loc, npath, hv))
    except Exception as e:
        print(file, str(e))


if __name__ == '__main__':
    with open('target/01/found-java-files.txt', 'r') as f:
        files = f.readlines()
    if not os.path.isdir('02'):
        os.makedirs('02')
    with open(OUT_FILE_NAME, 'w+') as f:
        f.write('file;cc;loc;npath\n')
    for i in range(THREADS_NUM):
        x = threading.Thread(target=process_files, args=(i, files))
        x.start()
