import os
import sys
sys.path.append('../metrics/cc')
sys.path.append('../metrics/loc')
from main import CCMetric
from loc import Loc
if not os.path.isdir('02'):
    os.makedirs('02')
f = open('02/metrics.csv', 'w+')
f.close()
f1 = open("01/found-java-files.txt", "r")
files = f1.readlines()
f1.close()
for file in files:
    try:
        m = CCMetric(file[:-1])
        cc = m.value(True)['data'][0]['complexity']
        l = Loc(file[:-1])
        loc = l.value()
        f = open('02/metrics.csv', 'a')
        f.write('{};{};{}\n'.format(file[:-1], cc, loc))
        f.close()
    except Exception as e:
        print(file, str(e))
