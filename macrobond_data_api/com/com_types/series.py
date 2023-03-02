# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body

from typing import List, Tuple
from datetime import datetime

from .entity import Entity
from .metadata import Metadata


class Series(Entity):
    """Interface for a Macrobond time series."""

    @property
    def Values(self) -> Tuple[float, ...]:
        """The values of the series."""

    @property
    def DatesAtStartOfPeriod(self) -> Tuple[datetime, ...]:
        """The dates of of the observations at the start of each period."""

    @property
    def DatesAtEndOfPeriod(self) -> Tuple[datetime, ...]:
        """The dates of of the observations at the end of each period."""

    @property
    def ForecastFlags(self) -> List[bool]:
        """A vector with a flag for each value indicating if this is a forecast or not."""

    @property
    def StartDate(self) -> datetime:
        """The start date."""

    @property
    def EndDate(self) -> datetime:
        """The end date."""

    @property
    def Frequency(self) -> int:
        """The calendar frequency."""

    @property
    def Weekdays(self) -> int:
        """The days of the week used for daily series."""

    @property
    def TypicalObservationCountPerYear(self) -> float:
        """The typical number of observations per year."""

    @property
    def ValuesMetadata(self) -> List[Metadata]:
        """Get the meta data for the values."""

    def GetValueAtDate(self, dateTime: datetime) -> float:
        """Get the value at or preceding a specific date."""

    def GetIndexAtDate(self, dateTime: datetime) -> int:
        """Get the index in the value vector at the specified date. Zero based."""
