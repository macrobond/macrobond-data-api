# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union, TYPE_CHECKING
from typing_extensions import Literal

from .api import Api
TypeVarApi = TypeVar('TypeVarApi', bound=Api)

if TYPE_CHECKING:
    from .credentials import Credentials


class Client(ABC, Generic[TypeVarApi]):

    def __init__(
        self,
        credentials: Union['Credentials', Literal[False]] = None  # pylint: disable=unused-argument
    ) -> None:
        ...  # pragma: no cover

    def __enter__(self) -> TypeVarApi:
        return self.open()  # pragma: no cover

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.close()  # pragma: no cover

    @abstractmethod
    def open(self) -> TypeVarApi:
        ...  # pragma: no cover

    @abstractmethod
    def close(self) -> None:
        ...  # pragma: no cover
