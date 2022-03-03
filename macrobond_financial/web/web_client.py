# -*- coding: utf-8 -*-

from typing import Optional, overload, Union, List

from macrobond_financial.common import Client, Credentials

from .session import Session, API_URL_DEFAULT, AUTHORIZATION_URL_DEFAULT
from .scope import Scope
from .web_api import WebApi


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

    @overload
    def __init__(
        self,
        client_id_or_credentials: str,
        client_secret: str,
        scopes: List[Scope] = None,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = AUTHORIZATION_URL_DEFAULT,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        client_id_or_credentials: Credentials,
        client_secret: str = ...,
        scopes: List[Scope] = None,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = AUTHORIZATION_URL_DEFAULT,
    ) -> None:
        ...

    @overload
    def __init__(
        self,
        client_id_or_credentials: str = None,
        client_secret: str = ...,
        scopes: List[Scope] = None,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = AUTHORIZATION_URL_DEFAULT,
    ) -> None:
        ...

    def __init__(
        self,
        client_id_or_credentials: Union[str, Credentials] = None,
        client_secret: str = None,
        scopes: List[Scope] = None,
        api_url: str = API_URL_DEFAULT,
        authorization_url: str = AUTHORIZATION_URL_DEFAULT,
    ) -> None:
        if client_id_or_credentials is None:
            client_id_or_credentials = Credentials()

        if isinstance(client_id_or_credentials, Credentials):
            super().__init__(client_id_or_credentials)
            credentials = client_id_or_credentials
            client_id = credentials.client_id
            client_secret = credentials.client_secret
        else:
            super().__init__(False)
            client_id = client_id_or_credentials

        if client_id is None:
            raise ValueError("client_id is None")

        if client_secret is None:
            raise ValueError("client_secret is None")

        if scopes is None:
            scopes = []

        self.__api: Optional["WebApi"] = None
        self.__session = Session(
            client_id,
            client_secret,
            *scopes,
            api_url=api_url,
            authorization_url=authorization_url
        )

    def open(self) -> "WebApi":
        if self.__api is None:
            self.__session.fetch_token()
            self.__api = WebApi(self.__session)
        return self.__api

    def close(self) -> None:
        self.__session.close()
