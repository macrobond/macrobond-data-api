# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Any, Dict, overload
from abc import ABC, abstractmethod

from datetime import datetime

from ..typs import VintageSeries, GetEntitiesError

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetVintageSeriesReturn(ABC):
    def __init__(
        self,
        serie_name: str,
        time: datetime,
        _raise: bool,
    ) -> None:
        self._serie_name = serie_name
        self._time = time
        self._raise = _raise

    @abstractmethod
    def _object(self) -> VintageSeries:
        ...  # pragma: no cover

    def object(self) -> VintageSeries:
        series = self._object()
        if self._raise and series.is_error:
            raise GetEntitiesError(self._serie_name, series.error_message)
        return series

    def dict(self) -> Dict[str, Any]:
        return self._object().to_dict()

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: "pandas_typing.Axes" = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        return self.object().data_frame(*args, **kwargs)
