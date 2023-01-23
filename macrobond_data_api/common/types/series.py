# -*- coding: utf-8 -*-

from datetime import datetime

from typing import Any, Dict, Tuple, Optional, List, cast, MutableMapping, TYPE_CHECKING
from typing_extensions import Literal

from .entity import Entity, EntityColumnsLiterals

from .._get_pandas import _get_pandas

SeriesColumnsLiterals = Literal[EntityColumnsLiterals, "Values", "Dates"]

SeriesColumns = List[SeriesColumnsLiterals]

if TYPE_CHECKING:  # pragma: no cover
    from pandas import Series as PdSeries  # type: ignore


class Series(Entity):
    """Represents a Macrobond time series."""

    __slots__ = ("values", "dates")

    values: Tuple[Optional[float], ...]
    dates: Tuple[datetime, ...]

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        metadata: Optional[MutableMapping[str, Any]],
        values: Optional[Tuple[Optional[float], ...]],
        dates: Optional[Tuple[datetime, ...]],
    ) -> None:
        super().__init__(name, error_message, metadata)

        self.values = ...  # type: ignore
        """
        The values of the series.
        The number of values is the same as the number of `Series.dates`. 
        """
        self.dates = ...  # type: ignore
        """
        The dates of the periods corresponding to the values
        The number of dates is the same as the number of `Series.values`. 
        """

        if values is None:
            self.values = tuple()
            self.dates = tuple()
        else:
            self.values = values
            self.dates = cast(Tuple[datetime, ...], dates)

    def to_dict(self) -> Dict[str, Any]:
        if self.is_error:
            return {
                "Name": self.name,
                "ErrorMessage": self.error_message,
            }
        ret = {
            "Name": self.name,
            "Values": self.values,
            "Dates": self.dates,
        }
        self._add_metadata(ret)
        return ret

    def values_to_pd_series(self, name: str = None) -> "PdSeries":
        pandas = _get_pandas()
        name = name if name else self.name
        return pandas.Series(self.values, self.dates, name=name)

    def __eq__(self, other):
        return self is other or (
            isinstance(other, Series)
            and self.error_message == other.error_message
            and self.metadata == other.metadata
        )
