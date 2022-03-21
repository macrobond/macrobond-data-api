# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING
from abc import ABC, abstractmethod


if TYPE_CHECKING:  # pragma: no cover

    from pandas import DataFrame  # type: ignore

    from ..typs import (
        UnifiedSeries,
        UnifiedSeriesDict,
    )


class GetUnifiedSeriesReturn(ABC):
    @abstractmethod
    def object(self) -> "UnifiedSeries":
        ...

    @abstractmethod
    def dict(self) -> "UnifiedSeriesDict":
        ...

    @abstractmethod
    def data_frame(self, columns: List[str] = None) -> "DataFrame":
        ...
