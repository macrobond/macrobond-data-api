from dataclasses import dataclass

from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, TYPE_CHECKING, Literal

if TYPE_CHECKING:  # pragma: no cover
    from pandas import Series, DataFrame

SeriesObservationHistoryColumnsLiterals = Literal["ObservationDate", "Values", "TimeStamps"]

SeriesObservationHistoryColumns = List[SeriesObservationHistoryColumnsLiterals]

__pdoc__ = {
    "SeriesObservationHistory.__init__": False,
}


@dataclass(init=False)
class SeriesObservationHistory:
    """The history of changes of an observation"""

    __slots__ = (
        "observation_date",
        "values",
        "time_stamps",
    )

    observation_date: datetime
    values: Sequence[Optional[float]]
    time_stamps: Sequence[Optional[datetime]]

    def __init__(
        self,
        observation_date: datetime,
        values: List[Optional[float]],
        time_stamps: List[Optional[datetime]],
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
            "Value": self.values,
            "TimeStamps": self.time_stamps,
        }

    def to_pd_data_frame(self) -> "DataFrame":
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame({"values": self.values}, self.time_stamps, dtype="float64")

    def to_pd_series(self, name: str = None) -> "Series":
        import pandas  # pylint: disable=import-outside-toplevel

        name = name if name else str(self.observation_date)
        return pandas.Series(self.values, self.time_stamps, name=name, dtype="float64")

    def _repr_html_(self) -> str:
        return self.to_pd_data_frame()._repr_html_()
