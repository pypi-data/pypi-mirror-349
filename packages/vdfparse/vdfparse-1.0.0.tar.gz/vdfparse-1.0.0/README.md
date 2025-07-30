# VDFParse

A Python parser for Valve Data Format (VDF) files, as used by Steam and other Valve products.

## Installation

```sh
pip install vdfparse
```

## Usage

```python
from vdfparse import VDFParse

vdf = VDFParse('path/to/file.vdf')
print(vdf.ToString())
```

See the source code for more advanced usage and helper functions.
