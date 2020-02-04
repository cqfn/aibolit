import sys
sys.path.append('./aibolit/metrics/cc')
from main import CCMetric

input = 'test/anton.java'
showlog = True
metric = CCMetric(input, showlog)
print(metric.value)
