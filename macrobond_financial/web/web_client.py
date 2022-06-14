# -*- coding: utf-8 -*-

from typing import Optional, List

from macrobond_financial.common import Client

from .session import Session, API_URL_DEFAULT, AUTHORIZATION_URL_DEFAULT
from .scope import Scope
from .web_api import WebApi

DEFAULT_SERVICE_NAME = AUTHORIZATION_URL_DEFAULT

_keyring_import_error: Optional[ImportError] = None
try:
    import keyring as _keyring  # type: ignore
except ImportError as ex:
    _keyring_import_error = ex


class WebClient(Client["WebApi"]):
    """
    WebClient to get data from the web

    Parameters
    ----------
    client_id : str
        record that failed processing

    client_secret : str
        record that failed processing

    scopes : List[str], optional
        record that failed processing

    api_url : str, optional
        record that failed processing

    authorization_url : str, optional
        record that failed processing

    Returns
    -------
    WebClient
        WebClient instance

    Examples
    -------
    ```python
    with WebClient('client id', 'client secret') as api:
        # use the api here
    ```
    """

    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        scopes: List[Scope] = None,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = AUTHORIZATION_URL_DEFAULT,
        service_name: str = DEFAULT_SERVICE_NAME,
    ) -> None:
        super().__init__()

        if client_secret is None:
            if _keyring_import_error:
                raise _keyring_import_error

            credential = _keyring.get_credential(service_name, "")

            if credential is None:
                keyring_name = str(_keyring.get_keyring())
                raise ValueError("can not find the key in keyring " + keyring_name)

            if client_id is None:
                client_id = credential.username

            client_secret = credential.password
        else:
            if client_id is None:
                raise ValueError("client_id is None")

        if scopes is None:
            scopes = []

        self.__api: Optional["WebApi"] = None
        self.__session = Session(
            client_id, client_secret, *scopes, api_url=api_url, authorization_url=authorization_url
        )

    def open(self) -> "WebApi":
        if self.__api is None:
            self.__session.fetch_token()
            self.__api = WebApi(self.__session)
        return self.__api

    def close(self) -> None:
        self.__session.close()
