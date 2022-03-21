# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING
from abc import ABC, abstractmethod

from ..typs import UnifiedSeries, UnifiedSeriesDict

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


class GetUnifiedSeriesReturn(ABC):
    @abstractmethod
    def object(self) -> UnifiedSeries:
        ...

    @abstractmethod
    def dict(self) -> UnifiedSeriesDict:
        ...

    @abstractmethod
    def data_frame(self, columns: List[str] = None) -> "DataFrame":
        ...
