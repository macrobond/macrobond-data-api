# Macrobond data-api-python

Exposes a common API in Python for the Macrobobond Web and Client data APIs

[***API reference***](https://macrobond.github.io/data-api-python/docs/macrobond_financial/)

# Basic usage
```python
# web
from macrobond_financial.web import WebClient

with WebClient('client id', 'client secret') as api:
    series = api.series.get_one_series('usgdp')

# com
from macrobond_financial.com import ComClient

with ComClient() as api:
    series = api.series.get_one_series('usgdp')
```

# Features
* Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum.
* Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum.
* Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum.
* Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum.

# Installing -name- and Supported Versions
-name- is available on PyPI:

for web api
```console
$ python -m pip install -name- [web]
```
for com api
```console
$ python -m pip install -name- [com]
```

-name- officially supports Python 3.6+.

# Contributing
We welcome community pull requests for bug fixes, enhancements, and documentation.

# Getting support
Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum.
