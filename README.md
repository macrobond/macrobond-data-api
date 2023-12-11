<!-- markdownlint-disable -->
<div align="center">
    <a href="https://www.macrobond.com/">
        <img loading="lazy" aria-roledescription="brand logo" alt="Macrobond logo" src="https://macrobond.github.io/macrobond-data-api/assets/Macrobond_logo_Color.svg" width="30%">
    </a>
</div>

<h1 align="center">Macrobond Data API for Python</h1>

<p align="center">
    <a href="https://pypi.org/project/macrobond-data-api/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/macrobond-data-api">
    </a>
    <a href="https://pypi.org/project/macrobond-data-api/">
        <img alt="PyPI" src="https://img.shields.io/pypi/pyversions/macrobond-data-api.svg">
    </a>
    <a href="https://github.com/macrobond/macrobond-data-api/blob/main/LICENSE">
        <img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg">
    </a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://github.com/macrobond/macrobond-data-api/actions/workflows/ci.yml">
        <img alt="Continuous Integration" src="https://github.com/macrobond/macrobond-data-api/actions/workflows/ci.yml/badge.svg">
    </a>
    <!--
    <a href="https://github.com/macrobond/macrobond-data-api/actions/workflows/deploying-github-pages.yaml">
        <img alt="Deploy to Github Pages" src="https://github.com/macrobond/macrobond-data-api/actions/workflows/deploying-github-pages.yaml/badge.svg">
    </a>
    <a href="https://github.com/macrobond/macrobond-data-api/actions/workflows/deploying-github-pages.yaml">
        <img alt="Deploy to PyPI" src="https://github.com/macrobond/macrobond-data-api/actions/workflows/python-publish.yml/badge.svg">
    </a>
    -->
</p>
<!-- markdownlint-enable -->

The Macrobond Data API for Python is used to access the world’s most extensive
macroeconomic, aggregate financial and sector database provided by [Macrobond](http://www.macrobond.com).
Exposes a common API in Python for the
[Macrobond Web](https://help.macrobond.com/technical-information/the-macrobond-data-web-api-feed/)
and [Client data](https://help.macrobond.com/technical-information/the-macrobond-api-for-python/)
APIs

You have to be a licensed user and have a Data+ or data feed user account in
order to use the API.

[***Examples in Jupyter Notebooks*** to help you get started](https://github.com/macrobond/macrobond-data-api/tree/main/examples)

[***API reference***](https://macrobond.github.io/macrobond-data-api/)

## Basic usage

```python
import macrobond_data_api as mb_api

usgdp = mb_api.get_one_series("usgdp")
```

## Advanced usage

```python
# web
from macrobond_data_api.web import WebClient

with WebClient('client id', 'client secret') as api:
    series = api.get_one_series('usgdp')

# com
from macrobond_data_api.com import ComClient

with ComClient() as api:
    series = api.get_one_series('usgdp')
```

## Features

The Macrobond Data API for Python uses either the
[Macrobond Web REST API](https://help.macrobond.com/technical-information/the-macrobond-data-web-api-feed/)
or the [Macrobond Client data API](https://help.macrobond.com/technical-information/the-macrobond-api-for-python/)
to obtain time series with values and metadata.
The API consists of a set of functions in common between the underlying APIs as
well as specialized functions unique to each implementation.

## Installing macrobond-data-api and Supported Versions

Macrobond Data API for Python is available on [PyPI](https://pypi.org/project/macrobond-data-api/):

```console
python -m pip install macrobond-data-api
```

Macrobond Data API for Python officially supports Python 3.8+.

## Using of system keyring for http proxy

For users operating behind an HTTP proxy, it is advisable to utilize the system keyring to store proxy settings and
credentials.
This can be conveniently accomplished by executing the included script with the following command:

```console
python -c "from macrobond_data_api.util import *; save_proxy_to_keyring()"
```

## Using of system keyring for credentials

> [!NOTE] 
> If u are using a proxy see "Using of system keyring for http proxy" first.

When using WebClient it is recommended to use the system keyring to store the API credentials.
This can be done easily by running the include script using this command:

```console
python -c "from macrobond_data_api.util import *; save_credentials_to_keyring()"
```

### Supported keyrings

* macOS [Keychain](https://en.wikipedia.org/wiki/Keychain_%28software%29)
* Freedesktop [Secret Service](http://standards.freedesktop.org/secret-service/)
supports many DE including GNOME (requires [secretstorage](https://pypi.python.org/pypi/secretstorage))
* KDE4 & KDE5 [KWallet](https://en.wikipedia.org/wiki/KWallet) (requires [dbus](https://pypi.python.org/pypi/dbus-python))
* [Windows Credential Locker](https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker)

## Contributing

We welcome community pull requests for bug fixes, enhancements, and documentation.

## Getting support

[Support options](https://help.macrobond.com/support/)
