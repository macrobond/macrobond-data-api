from typing import Optional, List

from .values_response import ValuesResponse


class SeriesResponse(ValuesResponse):
    """A time series"""

    dates: Optional[List[str]]
    """The dates of the series or not specified if there was an error"""
