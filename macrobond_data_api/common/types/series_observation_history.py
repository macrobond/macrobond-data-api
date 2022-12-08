# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Tuple
from typing_extensions import Literal

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import Series, DataFrame  # type: ignore

SeriesObservationHistoryColumnsLiterals = Literal["ObservationDate", "Values", "TimeStamps"]

SeriesObservationHistoryColumns = List[SeriesObservationHistoryColumnsLiterals]


class SeriesObservationHistory:
    """The history of changes of an observation"""

    __slots__ = (
        "observation_date",
        "values",
        "time_stamps",
    )

    observation_date: datetime
    values: Tuple[Optional[float], ...]
    time_stamps: Tuple[Optional[datetime], ...]

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

    def to_pd_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()
        return pandas.DataFrame({"values": self.values}, self.time_stamps)

    def to_pd_series(self, name: str = None) -> "Series":
        pandas = _get_pandas()
        name = name if name else str(self.observation_date)
        return pandas.Series(self.values, self.time_stamps, name=name)

    def __repr__(self):
        return f"{self.__class__.__name__} observation_date: {self.observation_date}"

    def __eq__(self, other):
        if not isinstance(other, SeriesObservationHistory):
            return NotImplemented

        return self is other or (
            self.observation_date == other.observation_date
            and self.values == other.values
            and self.time_stamps == other.time_stamps
        )
