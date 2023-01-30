<p align="center">
    <a href="https://www.macrobond.com/">
        <img src="https://assets-global.website-files.com/5fe1e5ab342569725c29e137/5fe3570b3d22be662c6a6276_macrobond-logo-white.webp" loading="lazy" aria-roledescription="brand logo" alt="Macrobond logo">
    </a>
</p>

<h1 align="center">Macrobond Data API for Python</h1>

<h1 align="center">This software is in beta !</h1>

<p align="center">
<a href="https://pypi.org/project/macrobond-data-api/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/macrobond-data-api">
</a>
<a href="https://pypi.org/project/macrobond-data-api/">
    <img alt="PyPI" src="https://img.shields.io/pypi/pyversions/macrobond-data-api.svg">
</a>
<!--
<a href="https://github.com/macrobond/macrobond-data-api/actions?query=workflow%3A%22tests%22">
    <img alt="PyPI" src="https://github.com/macrobond/macrobond-data-api/workflows/tests/badge.svg">
</a>
-->
<a href="https://github.com/macrobond-data-api/black/blob/main/LICENSE">
    <img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg">
</a>
<!--
<a href="https://pepy.tech/project/macrobond-data-api"><img alt="Downloads" src="https://pepy.tech/badge/macrobond-data-api">
</a>
-->
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
</p>


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

## Using of system keyring

When using WebClient it is recommended to use the system keyring.
This can be done easily by running the include script using this command:

```console
python -c "from macrobond_data_api.util import *; save_credential_to_keyring()"
```

### Supported keyrings

* macOS [Keychain](https://en.wikipedia.org/wiki/Keychain_%28software%29)
* Freedesktop [Secret Service](http://standards.freedesktop.org/secret-service/) supports many DE including GNOME (requires [secretstorage](https://pypi.python.org/pypi/secretstorage))
* KDE4 & KDE5 [KWallet](https://en.wikipedia.org/wiki/KWallet) (requires [dbus](https://pypi.python.org/pypi/dbus-python))
* [Windows Credential Locker](https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker)

## Contributing

We welcome community pull requests for bug fixes, enhancements, and documentation.

## Getting support

[Support options](https://help.macrobond.com/support/)
