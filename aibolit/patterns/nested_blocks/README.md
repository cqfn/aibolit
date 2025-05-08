Find in the code lines with the nested FOR/IF blocks of depth greater or equal to specified depth.
---

Python usage example:

```python
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType

pattern = NestedBlocks(2, block_type=BlockType.FOR)
lines = pattern.value('./file.java')
print(f'Lines where FOR loops of depth 2 is found: ${lines}')

pattern = NestedBlocks(2, block_type=BlockType.IF)
lines = pattern.value('./file.java')
print(f'Lines where IF blocks of depth 2 is found: ${lines}')
```
