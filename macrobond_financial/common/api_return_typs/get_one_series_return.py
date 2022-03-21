# -*- coding: utf-8 -*-

from typing import Union, overload, List, TYPE_CHECKING
from abc import ABC, abstractmethod


if TYPE_CHECKING:  # pragma: no cover

    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

    from ..typs import Series, SeriesColumns, SeriesTypedDict

    from typing_extensions import Literal

    SeriesValuesAndDatesColumns = List[Literal["Values", "Dates"]]


class GetOneSeriesReturn(ABC):
    @abstractmethod
    def object(self) -> "Series":
        ...

    @abstractmethod
    def dict(self) -> "SeriesTypedDict":
        ...

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["SeriesColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...

    @overload
    def values_and_dates_as_data_frame(self) -> "DataFrame":
        ...

    @overload
    def values_and_dates_as_data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["SeriesValuesAndDatesColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        ...
