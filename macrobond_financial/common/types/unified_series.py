# -*- coding: utf-8 -*-

from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Tuple,
    Optional,
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


class UnifiedSerie:
    """Interface for a Macrobond time series."""

    name: str
    error_message: str
    metadata: Dict[str, Any]
    values: Tuple[Optional[float], ...]

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
        """name"""

        self.error_message = error_message
        """error_message"""

        self.metadata = metadata
        """metadata"""

        self.values = values
        """values"""

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
            isinstance(other, UnifiedSerie)
            and self.name == other.name
            and self.error_message == other.error_message
            and self.values == other.values
            and self.metadata == other.metadata
        )


class UnifiedSeries(List[UnifiedSerie]):

    dates: Tuple[datetime, ...]

    @property
    def is_error(self) -> bool:
        return any(self)

    @property
    def series(self) -> List[UnifiedSerie]:
        return self

    def __init__(
        self,
        series: Sequence[UnifiedSerie],
        dates: Tuple[datetime, ...],
    ) -> None:
        super().__init__(series)
        self.dates = dates
        """dates"""

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
