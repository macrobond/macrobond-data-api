# Macrobond Data API for Python

The Macrobond Data API for Python is used to access the world’s most extensive macroeconomic, aggregate financial and sector database provided by [Macrobond](http://www.macrobond.com).
Exposes a common API in Python for the [Macrobobond Web](https://help.macrobond.com/technical-information/the-macrobond-web-api-data-feed/) and [Client data](https://help.macrobond.com/technical-information/the-macrobond-api-for-python/) APIs

You have to be a licensed user and have a Data+ or data feed user account in order to use the API.

[***API reference***](https://macrobond.github.io/macrobond-data-api/docs/macrobond-data-api)

## Basic usage

```python
# web
from macrobond_data_api.web import WebClient

with WebClient('client id', 'client secret') as api:
    series = api.series.get_one_series('usgdp')

# com
from macrobond_data_api.com import ComClient

with ComClient() as api:
    series = api.series.get_one_series('usgdp')
```

## Features

The Macrobond Data API for Python uses either the [Macrobond Web REST API](https://help.macrobond.com/technical-information/the-macrobond-web-api-data-feed/) or the [Macrobond Client data API](https://help.macrobond.com/technical-information/the-macrobond-api-for-python/) to obtain time series with values and metadata.
The API consists of a set of functions in common between the underlying APIs as well as specialized functions unique to each implementation.

## Installing macrobond-data-api and Supported Versions

Macrobond Data API for Python is available on PyPI:

```console
python -m pip install macrobond-data-api
```

Macrobond Data API for Python officially supports Python 3.6+.

## Contributing

We welcome community pull requests for bug fixes, enhancements, and documentation.

## Getting support

[Support options](https://help.macrobond.com/support/)
