from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Tuple,
    Optional,
    TYPE_CHECKING,
    overload,
)

from datetime import datetime
from typing_extensions import Literal, TypedDict


UnifiedSeriesColumnsLiterals = Literal["Dates", "Series"]

UnifiedSeriesColumns = List[UnifiedSeriesColumnsLiterals]

__pdoc__ = {
    "UnifiedSeriesDict.__init__": False,
    "UnifiedSeries.__init__": False,
    "UnifiedSeriesList.__init__": False,
}

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from .metadata import Metadata


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
    metadata: "Metadata"
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
        metadata: "Metadata",
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

    def __bool__(self) -> bool:
        return self.error_message == ""

    def __eq__(self, other: Any) -> bool:
        return self is other or (
            isinstance(other, UnifiedSeries)
            and self.name == other.name
            and self.error_message == other.error_message
            and self.values == other.values
            and self.metadata == other.metadata
        )


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
    dates: Tuple[datetime, ...]

    @property
    def is_error(self) -> bool:
        """
        True if any of the series has an error.
        """
        return any(self)

    def __init__(
        self,
        series: Sequence[UnifiedSeries],
        dates: Tuple[datetime, ...],
    ) -> None:
        super().__init__()
        self.series = series
        """The list of series"""
        self.dates = dates
        """The dates of the observations"""

    def to_dict(self) -> UnifiedSeriesDict:
        return {
            "Dates": self.dates,
            "Series": tuple(map(lambda x: x.to_dict(), self)),
        }

    def get_errors(self) -> Dict[str, str]:
        return {e.name: e.error_message for e in self if e.is_error}

    def to_pd_data_frame(self) -> "DataFrame":
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame({kv.name: kv.values for kv in self}, self.dates)

    def __repr__(self) -> str:
        names = ", ".join(map(lambda x: x.name, self))
        return f"UnifiedSeries series: ({names})"

    @overload
    def __getitem__(self, i: int) -> UnifiedSeries:
        ...

    @overload
    def __getitem__(self, s: slice) -> List[UnifiedSeries]:
        ...

    def __getitem__(self, key):  # type: ignore
        return self.series[key]

    def __len__(self) -> int:
        return len(self.series)