# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Optional
from win32com import client  # type: ignore

from macrobond_financial.common import Client

from .com_api import ComApi

if TYPE_CHECKING:  # pragma: no cover
    from .com_typs.connection import Connection


class ComClient(Client):
    __api: Optional['ComApi'] = None

    def open(self) -> 'ComApi':
        if self.__api is None:
            connection: 'Connection' = client.Dispatch("Macrobond.Connection")
            self.__api = ComApi(connection)
        return self.__api

    def close(self) -> None:
        '''
        free all resources used by the Macrobond API.
        Opening and closing sessions can be slow,
        so it is usually not a good idea to open and close them for each request
        '''
        if self.__api is not None:
            self.__api.connection.Close()
            self.__api = None
