from dataclasses import dataclass
from datetime import datetime

from typing import Optional

from macrobond_data_api.common.enums import (
    SeriesMissingValueMethod,
    SeriesToLowerFrequencyMethod,
    SeriesToHigherFrequencyMethod,
    SeriesPartialPeriodsMethod,
)

__pdoc__ = {
    "SeriesEntry.__init__": False,
}


@dataclass(init=False)
class SeriesEntry:
    """
    Properties of a series in a call to `macrobond_data_api.common.api.Api.get_unified_series`.
    """

    __slots__ = (
        "name",
        "vintage",
        "missing_value_method",
        "to_lower_frequency_method",
        "to_higher_frequency_method",
        "partial_periods_method",
    )

    def __init__(
        self,
        name: str,
        vintage: Optional[datetime] = None,
        missing_value_method: SeriesMissingValueMethod = SeriesMissingValueMethod.NONE,
        to_lower_frequency_method: SeriesToLowerFrequencyMethod = SeriesToLowerFrequencyMethod.AUTO,
        to_higher_frequency_method: SeriesToHigherFrequencyMethod = SeriesToHigherFrequencyMethod.AUTO,
        partial_periods_method: SeriesPartialPeriodsMethod = SeriesPartialPeriodsMethod.NONE,
    ) -> None:
        self.name = name
        """The name of the series."""

        self.vintage = vintage
        """Optional vintage of the series."""

        self.missing_value_method = missing_value_method
        """
        Method to use to fill in missing values.
        Should be a value of
        `macrobond_data_api.common.enums.series_missing_value_method.SeriesMissingValueMethod`
        """
        self.to_lower_frequency_method = to_lower_frequency_method
        """
        Method to use when converting to a lower frequency.
        Should be a value of
        `macrobond_data_api.common.enums.series_to_lower_frequency_method.SeriesToLowerFrequencyMethod`
        """

        self.to_higher_frequency_method = to_higher_frequency_method
        """
        Method to use when converting to a higher frequency.
        Should be a value of
        `macrobond_data_api.common.enums.series_to_higher_frequency_method.SeriesToHigherFrequencyMethod`
        """

        self.partial_periods_method = partial_periods_method
        """
        Method to use when converting partial periods to a lower frequency.
        Should be a value of
        `macrobond_data_api.common.enums.series_partial_periods_method.SeriesPartialPeriodsMethod`
        """
