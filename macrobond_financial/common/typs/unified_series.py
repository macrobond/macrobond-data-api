# -*- coding: utf-8 -*-

from typing import (
    Any,
    Dict,
    List,
    Sequence,
    Tuple,
    Optional,
    Union,
    overload,
    TYPE_CHECKING,
)

from datetime import datetime
from typing_extensions import Literal, TypedDict


from .._get_pandas import _get_pandas

UnifiedSeriesColumnsLiterals = Literal["Dates", "Series"]

UnifiedSeriesColumns = List[UnifiedSeriesColumnsLiterals]

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class UnifiedSeriesDict(TypedDict):
    Dates: Tuple[datetime, ...]
    Series: Tuple[Dict[str, Any], ...]


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


class UnifiedSeries(Sequence[UnifiedSerie]):
    @property
    def is_error(self) -> bool:
        return any(self.series)

    def __init__(
        self,
        dates: Tuple[datetime, ...],
        series: Tuple[UnifiedSerie, ...],
    ) -> None:
        self.dates = dates
        self.series = series

    def to_dict(self) -> UnifiedSeriesDict:
        return {
            "Dates": self.dates,
            "Series": tuple(map(lambda x: x.to_dict(), self.series)),
        }

    def get_errors(self) -> Dict[str, str]:
        return {
            e.name: e.error_message for e in filter(lambda x: x.is_error, self.series)
        }

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[UnifiedSeriesColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.to_dict()]
        return pandas.DataFrame(*args, **kwargs)

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

    def __bool__(self):
        return self.is_error

    def __eq__(self, other):
        return self is other or (
            isinstance(other, UnifiedSeries)
            and self.series == other.series
            and self.dates == other.dates
        )
