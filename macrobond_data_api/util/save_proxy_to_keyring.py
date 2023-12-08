#!/usr/bin/env python3

import traceback
import keyring

from requests import get

from macrobond_data_api.web.web_client import PROXY_USERNAME, DEFAULT_PROXY_SERVICE_NAME

from .save_credentials_to_keyring import _remove_duplicates, _test_keyring_backend
from .transfer_performance_test import _get_url


def save_proxy_to_keyring(warn_before_removing: bool = True, test_proxy: bool = True) -> bool:
    # fmt: off
    # pylint: disable=line-too-long
    """
    Create or update a proxy in the system's keyring interactively via the terminal.

    Parameters
    ----------
    warn_before_removing: bool
        Optional bool whether the method should ask before removing keys, default to `True`.

    test_proxy: bool
        Optional bool whether the method should test proxy before saving, default to `True`.

    Returns
    -------
    `bool`
    returns `True` if the key was successful created or update in the keyring.

    Remarks
    -------

    .. note::
    It's easy to run this method via the terminal.
    ```console  
    python -c "from macrobond_data_api.util import *; save_proxy_to_keyring()"
    ```

    .. caution::
    This method can remove proxy setting in your keyring, but it will ask first unless
    warn_before_removing is set to `False`.

    """
    # pylint: enable=line-too-long
    # fmt: on

    service_name = DEFAULT_PROXY_SERVICE_NAME
    username = PROXY_USERNAME

    if not _test_keyring_backend():
        return False

    keyring_name = keyring.get_keyring().name

    print("Saving secret to " + keyring_name + "\n")

    if not _remove_duplicates(service_name, username, warn_before_removing):
        return False

    print(
        "Proxy examples: ",
        " For a HTTPS Proxy use `https://10.10.1.10:1080` or `https://user:pass@10.10.1.10:1080`",
        " For a HTTP Proxy use `http://10.10.1.10:1080` or `http://user:pass@10.10.1.10:1080`",
        " For a Socks5 Proxy use `socks5://user:pass@host:port`",
        "",
        sep="\n",
    )

    proxy = input("Please enter proxy: ")

    if proxy == "":
        print("Removing proxy in keyring")
        if keyring.get_credential(service_name, username) is None:
            print("Proxy not found in keyring")
        else:
            keyring.delete_password(service_name, username)
        return True

    if test_proxy:
        print("Testing proxy")
        try:
            response = get(_get_url(1), proxies={"https": proxy, "http": proxy}, timeout=15)
            if response.status_code != 200:
                print(f"Error: failed testing proxy, got status code {response.status_code}")
                return False
        except Exception:  # pylint: disable=W0703
            print(traceback.format_exc())
            print("Error: failed failed testing proxy")
            return False

    print("Saving proxy to keyring")

    keyring.set_password(service_name, username, proxy)

    print(f'Successfully saved to the keyring with the service name: "{ service_name }" in {keyring_name}')

    return True


if __name__ == "__main__":
    save_proxy_to_keyring()
