import sys
sys.path.append('/home/zuoqin/java/aibolit/metrics/cc')
from main import CCMetric
input = 'tests/anton.java'
showlog = True
metric = CCMetric(input, showlog)
print(metric.value)
