# -*- coding: utf-8 -*-

from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Tuple,
    Optional,
    MutableMapping,
    TYPE_CHECKING,
)

from datetime import datetime
from typing_extensions import Literal, TypedDict


from .._get_pandas import _get_pandas

UnifiedSeriesColumnsLiterals = Literal["Dates", "Series"]

UnifiedSeriesColumns = List[UnifiedSeriesColumnsLiterals]

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


class UnifiedSeriesDict(TypedDict):
    Dates: Tuple[datetime, ...]
    Series: Tuple[Dict[str, Any], ...]


class UnifiedSeries:
    """
    Represents a Macrobond time series in the response from
    `macrobond_data_api.common.api.Api.get_unified_series`.
    """

    __slots__ = ("name", "error_message", "metadata", "values")

    name: str
    error_message: str
    metadata: MutableMapping[str, Any]
    values: Tuple[Optional[float], ...]

    @property
    def is_error(self) -> bool:
        """
        True if there was an error downloading this entity. `Entity.error_message` will
        contain any error message.
        """
        return self.error_message != ""

    def __init__(
        self,
        name: str,
        error_message: str,
        metadata: MutableMapping[str, Any],
        values: Tuple[Optional[float], ...],
    ) -> None:
        self.name = name
        """The name of the requested series."""

        self.error_message = error_message
        """Contains an error message if `UnifiedSerie.is_error` is True."""

        self.metadata = metadata
        """The metadata of the series."""

        self.values = values
        """The values of the series."""

    def to_dict(self) -> Dict[str, Any]:
        if self.is_error:
            return {
                "Name": self.name,
                "ErrorMessage": self.error_message,
            }
        ret = {
            "Name": self.name,
            "Values": self.values,
            "Metadata": self.metadata,
        }
        # self._add_metadata(ret)
        return ret

    def __bool__(self):
        return self.error_message == ""

    def __eq__(self, other):
        return self is other or (
            isinstance(other, UnifiedSeries)
            and self.name == other.name
            and self.error_message == other.error_message
            and self.values == other.values
            and self.metadata == other.metadata
        )


class UnifiedSeriesList(List[UnifiedSeries]):
    """
    The response from
    `macrobond_data_api.common.api.Api.get_unified_series`.
    """

    __slots__ = ("dates",)

    dates: Tuple[datetime, ...]

    @property
    def is_error(self) -> bool:
        """
        True if any of the series has an error.
        """
        return any(self)

    @property
    def series(self) -> List[UnifiedSeries]:
        """The list of series"""
        return self

    def __init__(
        self,
        series: Sequence[UnifiedSeries],
        dates: Tuple[datetime, ...],
    ) -> None:
        super().__init__(series)
        self.dates = dates
        """The dates of the observations"""

    def to_dict(self) -> UnifiedSeriesDict:
        return {
            "Dates": self.dates,
            "Series": tuple(map(lambda x: x.to_dict(), self)),
        }

    def get_errors(self) -> Dict[str, str]:
        return {e.name: e.error_message for e in filter(lambda x: x.is_error, self)}

    def to_pd_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()
        return pandas.DataFrame(dict(map(lambda kv: (kv.name, kv.values), self)), self.dates)

    def __repr__(self):
        names = ", ".join(map(lambda x: x.name, self))
        return f"UnifiedSeries series: ({names})"
