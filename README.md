# nested-attrs

[![CI](https://github.com/spenserblack/nested-attrs/actions/workflows/ci.yml/badge.svg)](https://github.com/spenserblack/nested-attrs/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/spenserblack/nested-attrs/branch/main/graph/badge.svg?token=XT5zP9lhqm)](https://codecov.io/gh/spenserblack/nested-attrs)

Just some small helpers for nested attributes.

## Example

```python
from nested_attrs import ngetattr as getattr
from nested_attrs import nsetattr as setattr

setattr(x, 'y.z', 'Hello, World!')
getattr(x, 'y.z') # 'Hello, World!
```
