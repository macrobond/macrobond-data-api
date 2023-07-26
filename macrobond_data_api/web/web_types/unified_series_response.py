from typing import List, Optional, TypedDict

from .values_response import ValuesResponse


class UnifiedSeriesResponse(TypedDict):
    """Response from a unified series request"""

    dates: Optional[List[str]]
    """The dates of the series or not specified if there were only errors"""

    series: List[ValuesResponse]
    """The list of series responses in the same order as in the request"""
