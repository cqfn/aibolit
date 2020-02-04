Metric calculated the number of FOR loops of greater or equal to specified depth
---


Terminal usage example:

```bash
$ python for_count.py file.java --for_max_depth=2
```



Python usage example:

```python
for_loop_n_metric = ForLoopNumber(2)
n = for_loop_n_metric.value('./file.java')
print(f'Number of FOR loops of depth 2 is ${n}')
```