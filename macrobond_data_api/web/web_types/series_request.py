from typing import Optional, TypedDict, List


class SeriesRequest(TypedDict, total=False):
    """A time series request"""

    values: List[Optional[float]]
    """The values of the series."""

    dates: Optional[List[str]]
    """
    The dates of the series or not specified if deducted from metadata. 
    When included, it must be the same length as the list of Values.
    """

    forecastFlags: Optional[List[bool]]
    """An optional array of forecast flags. When included, it must be the same length as the list of Values."""

    metadata: Optional[dict]
    """The metadata."""

    metadataBaseSeries: Optional[str]
    """An optional existing series to inherit metadata from."""
