Find variable declaration lines in the middle of its scope
---


Python usage example:

```python
pattern = VarMiddle()
lines = pattern.value('./file.java')
print(f'Variables are declared in the middle there: ${lines}')
```
