import os
import sys

if not os.path.isdir('02'):
    os.makedirs('02')
with open('01/found-java-files.txt', 'r') as f
    files = f.readlines()
for file in files:
    try:
        sys.path.append('../')
        from metrics.cc.main import CCMetric
        from metrics.loc.loc import Loc
        from metrics.npath.main import NPathMetric
        m = CCMetric(file[:-1])
        cc = m.value(True)['data'][0]['complexity']
        m = Loc(file[:-1])
        loc = m.value()
        m = NPathMetric(file[:-1])
        npath = m.value(True)['data'][0]['complexity']
        with open('02/file_metrics.csv', 'a+') as f:
            f.write('{};{};{};{}\n'.format(file[:-1], cc, loc, npath))
    except Exception as e:
        print(file, str(e))
