import os
import sys

if not os.path.isdir('02'):
    os.makedirs('02')
f = open('02/metrics.csv', 'w+')
f.close()
f1 = open("01/found-java-files.txt", "r")
files = f1.readlines()
f1.close()
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
        f = open('02/metrics.csv', 'a')
        f.write('{};{};{};{}\n'.format(file[:-1], cc, loc, npath))
        f.close()
    except Exception as e:
        print(file, str(e))
