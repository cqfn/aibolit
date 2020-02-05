Find in the code lines with the nested FOR loops of depth greater or equal to specified depth.
---

Python usage example:

```python
for_loop = ForNested(2)
lines = for_loop.value('./file.java')
print(f'Lines where FOR loops of depth 2 is found: ${lines}')
```