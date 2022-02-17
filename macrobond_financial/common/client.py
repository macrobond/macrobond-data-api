# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from logging import exception
from typing import Generic, TypeVar

from .api import Api

TypeVarApi = TypeVar('TypeVarApi', bound=Api)


class Client(ABC, Generic[TypeVarApi]):
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
