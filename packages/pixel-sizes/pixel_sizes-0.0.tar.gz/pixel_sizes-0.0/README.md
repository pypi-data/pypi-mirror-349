# python-pixel-sizes

[![codecov](https://codecov.io/gh/kitsuyui/python-pixel-sizes/graph/badge.svg?token=830WMASKHU)](https://codecov.io/gh/kitsuyui/python-pixel-sizes)

## Usage

```python
from pixel_sizes import SIZES

SIZES['Full HD'].width  # 1920
SIZES['Full HD'].height  # 1080
SIZES['Full HD'].aspect_ratio()  # 16/9 == 1.7777777777777777
SIZES['Full HD'].aspect_ratio_two()  # (16, 9)
```

# LICENSE

The 3-Clause BSD License. See also LICENSE file.
