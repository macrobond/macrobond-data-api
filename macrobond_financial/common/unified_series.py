# -*- coding: utf-8 -*-

from typing import (
    Any,
    Dict,
    Sequence,
    Tuple,
    Optional,
    Union,
    overload,
    TYPE_CHECKING,
)

from datetime import datetime

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore

    from typing_extensions import TypedDict

    class UnifiedSerieDict(TypedDict):
        name: str
        error_message: str
        metadata: Dict[str, Any]
        values: Tuple[Optional[float], ...]

    class UnifiedSeriesDict(TypedDict):
        dates: Tuple[datetime, ...]
        series: Tuple[UnifiedSerieDict, ...]


class UnifiedSerie:
    """Interface for a Macrobond time series."""

    @property
    def is_error(self) -> bool:
        return self.error_message != ""

    def __init__(
        self,
        name: str,
        error_message: str,
        metadata: Dict[str, Any],
        values: Tuple[Optional[float], ...],
    ) -> None:
        self.name = name
        self.error_message = error_message
        self.metadata = metadata
        self.values = values

    def __bool__(self):
        return self.error_message == ""


class UnifiedSeries(Sequence[UnifiedSerie]):
    def __init__(
        self,
        dates: Tuple[datetime, ...],
        series: Tuple[UnifiedSerie, ...],
    ) -> None:
        self.dates = dates
        self.series = series

    def __str__(self):
        return f"UnifiedSeries of {len(self)} series"

    def __repr__(self):
        return str(self)

    @overload
    def __getitem__(self, idx: int) -> UnifiedSerie:
        ...

    @overload
    def __getitem__(self, _slice: slice) -> Sequence[UnifiedSerie]:
        ...

    def __getitem__(self, idx_or_slice: Union[int, slice]):
        return self.series.__getitem__(idx_or_slice)

    def __len__(self) -> int:
        return len(self.series)
