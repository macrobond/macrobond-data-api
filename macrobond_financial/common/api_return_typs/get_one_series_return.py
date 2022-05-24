# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any, Dict, Union, overload, List, TYPE_CHECKING
from typing_extensions import Literal

from ..types import Series, SeriesColumns, GetEntitiesError

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

SeriesValuesAndDatesColumns = List[Literal["Values", "Dates"]]


class GetOneSeriesReturn(ABC):
    def __init__(self, series_name: str, _raise: bool) -> None:
        self._series_name = series_name
        self._raise = _raise

    @abstractmethod
    def _object(self) -> Series:
        ...

    def object(self) -> Series:
        series = self._object()
        if self._raise and series.is_error:
            raise GetEntitiesError(self._series_name, series.error_message)
        return series

    def dict(self) -> Dict[str, Any]:
        return self.object().to_dict()

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[SeriesColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        return self.object().data_frame(*args, **kwargs)

    @overload
    def values_and_dates_as_data_frame(self) -> "DataFrame":
        ...

    @overload
    def values_and_dates_as_data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[SeriesValuesAndDatesColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        return self.object().get_values_and_dates_as_data_frame(*args, **kwargs)
