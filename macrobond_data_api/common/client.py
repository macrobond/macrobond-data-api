# -*- coding: utf-8 -*-

"""
Base class for the implementations `macrobond_data_api.web.web_client.WebClient` and
`macrobond_data_api.com.com_client.ComClient`.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .api import Api

TypeVarApi = TypeVar("TypeVarApi", bound=Api)

__pdoc__ = {
    "Client.__init__": False,
}


class Client(ABC, Generic[TypeVarApi]):
    def __init__(self) -> None:
        ...  # pragma: no cover

    def __enter__(self) -> TypeVarApi:
        return self.open()  # pragma: no cover

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.close()  # pragma: no cover

    @property
    @abstractmethod
    def is_open(self) -> bool:
        ...

    @abstractmethod
    def open(self) -> TypeVarApi:
        ...  # pragma: no cover

    @abstractmethod
    def close(self) -> None:
        ...  # pragma: no cover

    def __repr__(self):
        return f"{self.__class__.__name__} is_open: {self.is_open}"
