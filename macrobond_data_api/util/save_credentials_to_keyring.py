#!/usr/bin/env python3
import sys
import json
import traceback
from getpass import getpass

import keyring
from keyring.backends.fail import Keyring as fail_keyring_backend
from keyring.backends.null import Keyring as null_keyring_backend
from macrobond_data_api.web.web_client import DEFAULT_SERVICE_NAME, DARWIN_USERNAME, WebClient


def _inquiry(question: str, default: str = "yes") -> bool:
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        if choice in valid:
            return valid[choice]
        sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def _remove_duplicates(service_name: str, username: str, warn_before_removing: bool) -> bool:
    old_credential = keyring.get_credential(service_name, username)
    while old_credential:
        if warn_before_removing and not _inquiry(
            'Warning - There is already a key with the same service name, it has the username "'
            + old_credential.username
            + '" can we remove it ? '
        ):
            return False
        keyring.delete_password(service_name, old_credential.username)
        old_credential = keyring.get_credential(service_name, username)
    return True


def _test_keyring_backend() -> bool:
    try:
        keyring_backend = keyring.get_keyring()
    except Exception:  # pylint: disable=W0703
        print(traceback.format_exc())
        print("Error: failed to get keyring")
        return False

    if isinstance(keyring_backend, null_keyring_backend):
        print("Error: keyring_backend is null_keyring_backend")
        return False

    if isinstance(keyring_backend, fail_keyring_backend):
        print("Error: keyring_backend is fail_keyring_backend")
        return False

    return True


def save_credentials_to_keyring(warn_before_removing: bool = True, ask_for_service_name: bool = False) -> bool:
    # fmt: off
    # pylint: disable=line-too-long
    """
    Create or update the credentials for the API in the system's keyring interactively via the  terminal.

    By defult the method will ask interactively for:
    * username, is the user's Macrobond Web Api username.
    * password, is the user's Macrobond Web Api password.

    If ask_for_service_name is `True`, then it will also ask for a service name.
    The service name becomes the name of the key in the user's keyring.

    Parameters
    ----------
    warn_before_removing: bool
        Optional bool whether the method should ask before removing keys, default to `True`.

    ask_for_service_name: bool
        Optional bool whether the method should ask for a service name to use, default to `False`.

    Returns
    -------
    `bool`
    returns `True` if the key was successful created or update in the keyring.

    Remarks
    -------

    .. note::
    It is easy to run this method via the terminal.
    ```console  
    python -c "from macrobond_data_api.util import *; save_credentials_to_keyring()"
    ```

    .. caution::
    This method can remove keys in your keyring, but it will ask first by default about warn_before_removing is `True`.

    Supported keyrings
    ------------------
    * macOS [Keychain](https://en.wikipedia.org/wiki/Keychain_%28software%29)
    * Freedesktop [Secret Service](http://standards.freedesktop.org/secret-service/) supports many DE including GNOME (requires [secretstorage](https://pypi.python.org/pypi/secretstorage))
    * KDE4 & KDE5 [KWallet](https://en.wikipedia.org/wiki/KWallet) (requires [dbus](https://pypi.python.org/pypi/dbus-python))
    * [Windows Credential Locker](https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker)

    """
    # pylint: enable=line-too-long
    # fmt: on

    if not _test_keyring_backend():
        return False

    is_darwin = sys.platform.startswith("darwin")
    keyring_name = keyring.get_keyring().name

    print("Saving secret to " + keyring_name + "\n")

    service_name = (
        input(
            "Please enter the service name or just pressure 'enter' to use the default one ("
            + DEFAULT_SERVICE_NAME
            + "): "
        )
        if ask_for_service_name
        else ""
    )
    if service_name == "":
        service_name = DEFAULT_SERVICE_NAME

    if not _remove_duplicates(service_name, DARWIN_USERNAME if is_darwin else "", warn_before_removing):
        return False

    username = input("Please enter Macrobond Web Api username: ")
    password = getpass("Please enter Macrobond Web Api password: ")

    print("Testing username and password")
    try:
        with WebClient(username=username, password=password) as api:
            api.metadata_get_attribute_information("PrimName")
    except Exception:  # pylint: disable=W0703
        print(traceback.format_exc())
        print("Error: failed testing username and password")
        return False

    if is_darwin:
        keyring.set_password(service_name, DARWIN_USERNAME, json.dumps({"username": username, "password": password}))
    else:
        keyring.set_password(service_name, username, password)

    print("Testing keyring")
    try:
        with WebClient() as api:
            api.metadata_get_attribute_information("PrimName")
    except Exception:  # pylint: disable=W0703
        print(traceback.format_exc())
        print("Error: failed testing keyring")
        return False

    print(f'Successfully saved to the keyring with the service name: "{ service_name }" in {keyring_name}')

    return True


if __name__ == "__main__":
    save_credentials_to_keyring()
