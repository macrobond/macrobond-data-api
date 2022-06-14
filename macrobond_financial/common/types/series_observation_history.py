# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Tuple, Union, overload
from typing_extensions import Literal

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

SeriesObservationHistoryColumnsLiterals = Literal["ObservationDate", "Values", "TimeStamps"]

SeriesObservationHistoryColumns = List[SeriesObservationHistoryColumnsLiterals]


class SeriesObservationHistory:
    """The history of changes of an observation"""

    def __init__(
        self,
        observation_date: datetime,
        values: Tuple[Optional[float], ...],
        time_stamps: Tuple[Optional[datetime], ...],
    ) -> None:
        self.observation_date = observation_date
        """The date of the observation"""

        self.values = values
        """
        The historical values of the observation or an empty tuple if
        there are no recorded values for the specified date.
        """

        self.time_stamps = time_stamps
        """
        A tuple of timestamps of when the historical values were recorded.
        The first timestamp may be null if the time of the original is unknown.
        """

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ObservationDate": self.observation_date,
            "Values": self.values,
            "TimeStamps": self.time_stamps,
        }

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[SeriesObservationHistoryColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.to_dict()]
        return pandas.DataFrame(*args, **kwargs)

    def get_values_and_time_stamps_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        kwargs["data"] = {
            "Values": self.values,
            "Dates": self.time_stamps,
        }
        args = args[1:]
        return pandas.DataFrame(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__} {self.observation_date}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, SeriesObservationHistory):
            return NotImplemented

        return self is other or (
            self.observation_date == other.observation_date
            and self.values == other.values
            and self.time_stamps == other.time_stamps
        )
