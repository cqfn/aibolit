import sys
from main import CCMetric
sys.path.append('/home/zuoqin/java/aibolit/metrics/cc')

input = 'tests/anton.java'
showlog = True
metric = CCMetric(input, showlog)
print(metric.value)
