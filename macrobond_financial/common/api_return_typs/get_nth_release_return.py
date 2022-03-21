# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING, overload
from abc import ABC, abstractmethod


if TYPE_CHECKING:  # pragma: no cover

    from ..typs.series import (
        Series,
        SeriesTypedDict,
    )

    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetNthReleaseReturn(ABC):
    @abstractmethod
    def object(self) -> "Series":
        ...  # pragma: no cover

    @abstractmethod
    def dict(self) -> "SeriesTypedDict":
        ...  # pragma: no cover

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

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...  # pragma: no cover
