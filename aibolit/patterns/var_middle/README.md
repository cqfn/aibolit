Find variable declaration lines in the middle of method
---

Limitations:

 - javalang library have issues to correctly display line number for statements
 - does not work with nested methods declarations

Python usage example:

```python
pattern = VarMiddle()
lines = pattern.value('./file.java')
print(f'Variables are declared in the middle there: ${lines}')
```