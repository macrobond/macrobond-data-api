# -*- coding: utf-8 -*-

from typing import overload, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class _ReturnDataFrame(ABC):

    @overload
    def data_frame(self) -> 'DataFrame': ...

    @overload
    def data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: 'pandas_typing.Axes' = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @overload
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...
