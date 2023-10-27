"""
Base class for the implementations `macrobond_data_api.web.web_client.WebClient` and
`macrobond_data_api.com.com_client.ComClient`.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .api import Api

TypeVarApi = TypeVar("TypeVarApi", bound=Api)

__pdoc__ = {
    "Client.__init__": False,
}


class Client(ABC, Generic[TypeVarApi]):
    def __init__(self) -> None:
        pass  # pragma: no cover

    def __enter__(self) -> TypeVarApi:
        return self.open()  # pragma: no cover

    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None:
        self.close()  # pragma: no cover

    @property
    @abstractmethod
    def is_open(self) -> bool:
        ...  # pragma: no cover

    @abstractmethod
    def open(self) -> TypeVarApi:
        ...  # pragma: no cover

    @abstractmethod
    def close(self) -> None:
        ...  # pragma: no cover

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} is_open: {self.is_open}"
