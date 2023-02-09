# pylint: disable = invalid-name , missing-module-docstring
# mypy: disable_error_code = empty-body

from typing import Optional
from datetime import datetime

from macrobond_data_api.common.enums import (
    SeriesMissingValueMethod,
    SeriesToLowerFrequencyMethod,
    SeriesToHigherFrequencyMethod,
    SeriesPartialPeriodsMethod,
)


class SeriesExpression:
    """Interface for a Macrobond series expression."""

    @property
    def Name(self) -> str:
        """Get the name of the series."""

    @Name.setter
    def Name(self, new_name: str) -> None:
        """Set the name of the series."""

    @property
    def MissingValueMethod(self) -> SeriesMissingValueMethod:
        """Get the method for filling in missing values."""

    @MissingValueMethod.setter
    def MissingValueMethod(self, new_missing_value_method: SeriesMissingValueMethod) -> None:
        """Set the method for filling in missing values."""

    @property
    def ToLowerFrequencyMethod(self) -> SeriesToLowerFrequencyMethod:
        """Get the method to converting to lower frequency."""

    @ToLowerFrequencyMethod.setter
    def ToLowerFrequencyMethod(self, new_missing_value_method: SeriesToLowerFrequencyMethod) -> None:
        """Set the method to converting to lower frequency."""

    @property
    def ToHigherFrequencyMethod(self) -> SeriesToHigherFrequencyMethod:
        """Get the method to converting to higher frequency."""

    @ToHigherFrequencyMethod.setter
    def ToHigherFrequencyMethod(self, new_missing_value_method: SeriesToHigherFrequencyMethod) -> None:
        """Set the method to converting to higher frequency."""

    @property
    def PartialPeriodsMethod(self) -> SeriesPartialPeriodsMethod:
        """Get the method to use for converting partial periods to lower frequency."""

    @PartialPeriodsMethod.setter
    def PartialPeriodsMethod(self, new_missing_value_method: SeriesPartialPeriodsMethod) -> None:
        """Set the method to use for converting partial periods to lower frequency."""

    @property
    def Vintage(self) -> Optional[datetime]:
        """Get the vintage date of the series."""

    @Vintage.setter
    def Vintage(self, new_vintage: Optional[datetime]) -> None:
        """Set the vintage date of the series."""
