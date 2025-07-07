# Cyclomatic Complexity metric for Java code analysis.

Usage:

```python
from aibolit.metrics.cc.main import CCMetric
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast

ast = AST.build_from_javalang(build_ast('MyClass.java'))
metric = CCMetric()
complexity = metric.value(ast)
print(f"Total cyclomatic complexity: {complexity}")
```
