# -*- coding: utf-8 -*-

from typing import Optional, List

from macrobond_data_api.common import Client

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
    username : str, optional
        The username to use for authentication.
        If not specified, an attempt is made to get the credentials from the keyring

    password : str, optional
        The password to use for authentication.
        If not specified, an attempt is made to get the credentials from the keyring

    scopes : List[str], optional
        A list of scopes to request as part of the authorization.
        If not specified, all available scopes will be requested.
        The common scopes requires are "macrobond_web_api.read_mb" and "macrobond_web_api.search_mb"

    api_url : str, optional
        The URL of the API.
        If not specified, the default URL will be used, which is what you want in most cases.

    authorization_url : str, optional
        The URL of the authorization server.
        If not specified, the default URL will be used, which is what you want in most cases.

    proxy : str, optional
        For a HTTPS Proxy use `https://10.10.1.10:1080` or `https://user:pass@10.10.1.10:1080`
        For a HTTP Proxy use `http://10.10.1.10:1080` or `http://user:pass@10.10.1.10:1080`
        For a Socks5 Proxy use `socks5://user:pass@host:port`

    Returns
    -------
    WebClient
        The WebClient instance

    Examples
    -------
    ```python
    # use credentials stored in the keyring
    with WebClient() as api:
        # use the api here
    ```
    ```python
    with WebClient('client id', 'client secret') as api:
        # use the api here
    ```
    """

    def __init__(
        self,
        username: str = None,
        password: str = None,
        scopes: List[Scope] = None,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = AUTHORIZATION_URL_DEFAULT,
        service_name: str = DEFAULT_SERVICE_NAME,
        proxy: str = None,
    ) -> None:
        super().__init__()

        if password is None:
            if _keyring_import_error:
                raise _keyring_import_error

            credential = _keyring.get_credential(service_name, "")

            if credential is None:
                keyring_name = str(_keyring.get_keyring())
                raise ValueError("can not find the key in keyring " + keyring_name)

            if username is None:
                username = credential.username

            password = credential.password
        else:
            if username is None:
                raise ValueError("username is None")

        if scopes is None:
            scopes = []

        self.__api: Optional["WebApi"] = None
        self.__session = Session(
            username,
            password,
            *scopes,
            api_url=api_url,
            authorization_url=authorization_url,
            proxy=proxy
        )

    @property
    def is_open(self) -> bool:
        return bool(self.__api)

    def open(self) -> "WebApi":
        if self.__api is None:
            self.__session.fetch_token()
            self.__api = WebApi(self.__session)
        return self.__api

    def close(self) -> None:
        self.__session.close()
