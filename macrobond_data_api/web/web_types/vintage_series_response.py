from typing import Optional

from .series_with_times_of_change_response import SeriesWithTimesOfChangeResponse


class VintageSeriesResponse(SeriesWithTimesOfChangeResponse):
    """A time series with times of change"""

    vintageTimeStamp: Optional[str]
    """The time when this version of the series was recorded"""
