from typing import List, Optional, TypedDict

from macrobond_data_api.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarDateMode,
    CalendarMergeMode,
    SeriesMissingValueMethod,
    SeriesToLowerFrequencyMethod,
    SeriesToHigherFrequencyMethod,
    SeriesPartialPeriodsMethod,
)


class UnifiedSeriesEntry(TypedDict):
    """Request of a list of series converted to the same calendar"""

    name: str
    """The name of the series."""

    vintage: Optional[str]
    """The vintage of the series. The default is the latest version of the series."""

    missingValueMethod: Optional[SeriesMissingValueMethod]
    """The method for filling in missing values. The default is the automatic method."""

    toLowerFrequencyMethod: Optional[SeriesToLowerFrequencyMethod]
    """The method to converting to lower frequency.  The default is the automatic method."""

    toHigherFrequencyMethod: Optional[SeriesToHigherFrequencyMethod]
    """The method to converting to higher frequency. The default is the automatic method."""

    partialPeriodsMethod: Optional[SeriesPartialPeriodsMethod]
    """
    The method to use for converting partial periods to lower frequency.
    The default is not to extend the series.
    """


class UnifiedSeriesRequest(TypedDict, total=False):
    """Request of a list of series converted to the same calendar"""

    frequency: Optional[SeriesFrequency]
    """
    The frequency to convert all series to.
    The default is to convert to the highest frequency of the series in the request.
    """

    weekdays: Optional[SeriesWeekdays]
    """The days of the week used for daily series. The default is Monday to Friday."""

    calendarMergeMode: Optional[CalendarMergeMode]
    """
    The merge mode determines how the series calendars are used when forming the new
    shared calendar.
    The default is to use all observations that are in any calendar.
    """

    currency: Optional[str]
    """The currency to use for currency conversion or omitted for no conversion."""

    startDateMode: Optional[CalendarDateMode]
    """
    The start date mode determines how the start date is calculated.
    By default the mode is to start when there is data in any series.
    """

    startPoint: Optional[str]
    """
    The start point. By default, this is determined by the startDateMode.
    It can be a date on the format yyyy-mm-dd or a number of observations relative the end of
    the series.
    """

    endDateMode: Optional[CalendarDateMode]
    """
    The end date mode determines how the end date is calculated.
    By default the mode is to end when there is no data in any series.
    """

    endPoint: Optional[str]
    """
    The end point. By default, this is determined by the endDateMode.
    It can be a date on the format yyyy-mm-dd or a number of observations relative the
    end of the series.
    """

    seriesEntries: List[UnifiedSeriesEntry]
    """The list of series entries that defines the series to request."""
