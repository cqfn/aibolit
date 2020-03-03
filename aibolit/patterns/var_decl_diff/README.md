Find lines in the source file where line distance between variable declaration
and its first usage is longer than some threshold
---

Python usage example:

```python
pattern = VarDiffFirstDeclarationAndUsage(lines_th=4)
lines = pattern.value('./file.java')
print(f'Variables are declared far away: ${lines}')
```