# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

from getpass import getpass

import sys
import keyring
from macrobond_financial.web.web_client import DEFAULT_SERVICE_NAME


def save_credential_to_keyring() -> None:
    KEYRING_NAME = keyring.get_keyring().__class__.__name__

    print("Saving secret to " + KEYRING_NAME + "\n")

    service_name = input(
        "Please enter the service name or just enter to save to default name ("
        + DEFAULT_SERVICE_NAME
        + "): "
    )
    if service_name == "":
        service_name = DEFAULT_SERVICE_NAME

    if keyring.get_credential(service_name, ""):
        print(
            "Multiple keys Error\n"
            + "Possible reasons for the error:\n"
            + "\tService name already exists\n"
            + "\tService name prefix with with a user name exists\n",
            file=sys.stderr,
        )
        sys.exit(1)

    client_id = input("Please enter the client id: ")

    client_secret = getpass("Please enter the client secret: ")

    keyring.set_password(service_name, client_id, client_secret)


if __name__ == "__main__":
    save_credential_to_keyring()
