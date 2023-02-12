#!/usr/bin/env python3
import sys
import json
from getpass import getpass

import keyring
from macrobond_data_api.web.web_client import (
    DEFAULT_SERVICE_NAME,
    DARWIN_USERNAME,
)


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


def save_credential_to_keyring(warn_before_removing: bool = True, ask_for_service_name: bool = False) -> bool:
    # fmt: off
    # pylint: disable=line-too-long
    """
    Create or update a key in the system's keyring interactively via terminal.

    By defult the method will ask interactively for:
    * username, username is the user's Macrobond Web Api username.
    * password, password is the user's Macrobond Web Api password.

    If ask_for_service_name is `True`, then it will also ask for a service name.
    a service name becomes the name of the key in the user's keyring.

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
    It's easy to run this method via the terminal.
    ```console  
    python -c "from macrobond_data_api.util import *; save_credential_to_keyring()"
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

    if is_darwin:
        keyring.set_password(service_name, DARWIN_USERNAME, json.dumps({"username": username, "password": password}))
    else:
        keyring.set_password(service_name, username, password)

    print(f'successfully saved to the keyring with the service name: "{ service_name }" in {keyring_name}')

    return True


if __name__ == "__main__":
    save_credential_to_keyring()
