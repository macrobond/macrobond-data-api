# -*- coding: utf-8 -*-

from typing import Optional

from macrobond_financial.common import Client

from .session import Session, API_URL_DEFAULT, AUTHORIZATION_URL_DEFAULT
from .scope import Scope
from .web_api import WebApi


class WebClient(Client):

    __api: Optional['WebApi'] = None

    def __init__(
            self, client_id: str, client_secret: str, *scopes: Scope,
            api_url: str = API_URL_DEFAULT, authorization_url: str = AUTHORIZATION_URL_DEFAULT
    ) -> None:
        super().__init__()
        self.__session = Session(
            client_id, client_secret, *scopes,
            api_url=api_url, authorization_url=authorization_url
        )

    def open(self) -> 'WebApi':
        if self.__api is None:
            self.__session.fetch_token()
            self.__api = WebApi(self.__session)
        return self.__api

    def close(self) -> None:
        self.__session.close()
