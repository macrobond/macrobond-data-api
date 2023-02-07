# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body

from datetime import datetime
from typing import List

from .series import Series


class SeriesWithRevisions:
    """Interface for a Macrobond series with revisions."""

    @property
    def IsError(self) -> bool:
        """Gets a value indicating whether the series request resulted in an error."""

    @property
    def ErrorMessage(self) -> str:
        """Gets the error message."""

    @property
    def HasRevisions(self) -> bool:
        """Check is there are any revisions."""

    @property
    def StoresRevisions(self) -> bool:
        """Check if underlying series stores revisions."""

    @property
    def TimeOfLastRevision(self) -> datetime:
        """Get the time of the last revision."""

    @property
    def Head(self) -> Series:
        """Get the series with the latest revisions."""

    def GetNthRelease(self, n: int) -> Series:
        """Get the series at the specified release."""

    def GetVintage(self, date: datetime) -> Series:
        """Get the series at the specified time."""

    def GetVintageDates(self) -> List[datetime]:
        """Get the times for all revisions."""

    def GetObservationHistory(self, pointInTime: datetime) -> Series:
        """Get the values over time for a specific point in time."""

    def GetCompleteHistory(self) -> List[Series]:
        """Get all the revisions as a separate complete series."""
