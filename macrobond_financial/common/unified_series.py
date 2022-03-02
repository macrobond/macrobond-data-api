# -*- coding: utf-8 -*-

from typing import Any, Dict, Sequence, Tuple, Optional, List, Union, cast, TYPE_CHECKING, overload

from datetime import datetime

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore

    from .entity import EntityColumnsLiterals, EntityTypedDict

    from typing_extensions import Literal

    UnifiedSeriesColumns = List[Literal[EntityColumnsLiterals, 'values']]

    class UnifiedSeriesTypedDict(EntityTypedDict):
        values: Tuple[Optional[float], ...]


class UnifiedSerie:
    '''Interface for a Macrobond time series.'''

    @property
    def is_error(self) -> bool:
        return self.error_message != ''

    def __init__(
        self,
        error_message: str,
        metadata: Optional[Dict[str, Any]],
        values: Optional[Tuple[Optional[float], ...]],
    ) -> None:
        self.error_message = error_message
        if error_message != '':
            self.metadata: Dict[str, Any] = {}
            self.values: Tuple[Optional[float], ...] = tuple()
        else:
            self.metadata = cast(Dict[str, Any], metadata)
            self.values = cast(Tuple[Optional[float], ...], values)


class UnifiedSeries(Sequence[UnifiedSerie]):

    def __init__(
        self,
        dates: Optional[Tuple[datetime, ...]],
        series: Tuple[UnifiedSerie, ...],
    ) -> None:
        self.dates = dates if dates is not None else tuple()
        self.series = series

    def __str__(self):
        return f'UnifiedSeries of {len(self)} series'

    def __repr__(self):
        return str(self)

    @overload
    def __getitem__(self, idx: int) -> UnifiedSerie: ...

    @overload
    def __getitem__(self, _slice: slice) -> Sequence[UnifiedSerie]: ...

    def __getitem__(self, idx_or_slice: Union[int, slice]):
        return self.series.__getitem__(idx_or_slice)

    def __len__(self) -> int:
        return len(self.series)
