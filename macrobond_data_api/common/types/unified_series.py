from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Optional, TYPE_CHECKING, overload, Literal, TypedDict

from datetime import datetime

UnifiedSeriesColumnsLiterals = Literal["Dates", "Series"]

UnifiedSeriesColumns = List[UnifiedSeriesColumnsLiterals]

__pdoc__ = {
    "UnifiedSeriesDict.__init__": False,
    "UnifiedSeries.__init__": False,
    "UnifiedSeriesList.__init__": False,
}

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame
    from .metadata import Metadata


class UnifiedSeriesDict(TypedDict):
    Dates: Sequence[datetime]
    Series: Sequence[Dict[str, Any]]


@dataclass(init=False)
class UnifiedSeries:
    """
    Represents a Macrobond time series in the response from
    `macrobond_data_api.common.api.Api.get_unified_series`.
    """

    __slots__ = ("name", "error_message", "metadata", "values")

    name: str
    error_message: str
    metadata: "Metadata"
    values: Sequence[Optional[float]]

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
        metadata: "Metadata",
        values: List[Optional[float]],
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

    def __bool__(self) -> bool:
        return self.error_message == ""


@dataclass(init=False)
class UnifiedSeriesList(Sequence[UnifiedSeries]):
    """
    The response from
    `macrobond_data_api.common.api.Api.get_unified_series`.
    """

    __slots__ = (
        "series",
        "dates",
    )

    series: Sequence[UnifiedSeries]
    dates: Sequence[datetime]

    @property
    def is_error(self) -> bool:
        """
        True if any of the series has an error.
        """
        return any(self)

    def __init__(
        self,
        series: List[UnifiedSeries],
        dates: List[datetime],
    ) -> None:
        super().__init__()
        self.series = series
        """The list of series"""
        self.dates = dates
        """The dates of the observations"""

    def to_dict(self) -> UnifiedSeriesDict:
        return {
            "Dates": self.dates,
            "Series": [x.to_dict() for x in self],
        }

    def get_errors(self) -> Dict[str, str]:
        return {e.name: e.error_message for e in self if e.is_error}

    def to_pd_data_frame(self) -> "DataFrame":
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame(
            {
                **{"date": self.dates},
                **{
                    "Error: " + kv.error_message
                    if kv.is_error
                    else kv.name: [None] * len(self.dates)  # type: ignore
                    if kv.is_error
                    else kv.values
                    for kv in self
                },
            }
        )

    def _repr_html_(self) -> str:
        return self.to_pd_data_frame()._repr_html_()

    @overload
    def __getitem__(self, i: int) -> UnifiedSeries:
        pass

    @overload
    def __getitem__(self, s: slice) -> List[UnifiedSeries]:
        pass

    def __getitem__(self, key):  # type: ignore
        return self.series[key]

    def __len__(self) -> int:
        return len(self.series)
