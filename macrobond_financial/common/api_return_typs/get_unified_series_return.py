# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Union, overload
from abc import ABC, abstractmethod

from ..types import (
    UnifiedSeries,
    UnifiedSeriesDict,
    GetEntitiesError,
    UnifiedSeriesColumns,
)

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetUnifiedSeriesReturn(ABC):
    def __init__(self, _raise: bool) -> None:
        self._raise = _raise

    @abstractmethod
    def _object(self) -> UnifiedSeries:
        ...

    def object(self) -> UnifiedSeries:
        ret = self._object()

        errors = ret.get_errors()
        if self._raise and len(errors) != 0:
            raise GetEntitiesError(errors)

        return ret

    def dict(self) -> UnifiedSeriesDict:
        return self.object().to_dict()

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[UnifiedSeriesColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        return self.object().data_frame(*args, **kwargs)
