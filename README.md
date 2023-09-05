[![Python application](https://github.com/doronz88/python-package/workflows/Python%20application/badge.svg)](https://github.com/doronz88/maclog/actions/workflows/python-app.yml "Python application action")
[![Pypi version](https://img.shields.io/pypi/v/python-package.svg)](https://pypi.org/project/maclog/ "PyPi package")
[![Downloads](https://static.pepy.tech/personalized-badge/python-package?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/maclog)

# Overview

Query macOS syslog from python3.


# Installation

```shell
python3 -m pip install -U maclog
```

# Usage

```python
from maclog.log import get_logger

for entry in get_logger():
    print(entry)
```

# Contributing

See [CONTRIBUTING](CONTRIBUTING.md).
