Find in code line with nested FOR loops of depth greater or equal to specified depth
---


Terminal usage example:

```bash
$ python for_count.py file.java --for_max_depth=2
```



Python usage example:

```python
for_loop_n_metric = ForNested(2)
lines = for_loop_n_metric.value('./file.java')
print(f'Number of FOR loops of depth 2 is ${n}')
```