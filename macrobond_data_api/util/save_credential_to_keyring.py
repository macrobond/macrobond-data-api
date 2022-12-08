# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

from getpass import getpass

import keyring
from macrobond_data_api.web.web_client import DEFAULT_SERVICE_NAME


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

    old_credential = keyring.get_credential(service_name, "")
    while old_credential:
        keyring.delete_password(service_name, old_credential.username)
        old_credential = keyring.get_credential(service_name, "")

    client_id = input("Please enter the client id: ")

    client_secret = getpass("Please enter the client secret: ")

    keyring.set_password(service_name, client_id, client_secret)


if __name__ == "__main__":
    save_credential_to_keyring()
