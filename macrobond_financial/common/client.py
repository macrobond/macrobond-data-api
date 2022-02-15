# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from .api import Api


class Client(ABC):
    def __enter__(self) -> Api:
        return self.open()  # pragma: no cover

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.close()  # pragma: no cover

    @abstractmethod
    def open(self) -> Api:
        ...  # pragma: no cover

    @abstractmethod
    def close(self) -> None:
        ...  # pragma: no cover
