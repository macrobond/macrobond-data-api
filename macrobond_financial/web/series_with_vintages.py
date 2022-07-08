# -*- coding: utf-8 -*-

from typing import Optional, Dict, Any, List
from dateutil import parser  # type: ignore

from .web_types import VintageValuesResponse, SeriesWithVintagesResponse


class VintageValues:
    """A time series with times of change"""

    __slots__ = ("vintage_time_stamp", "dates", "values")

    vintage_time_stamp: Optional[str]
    """The time when this version of the series was recorded"""

    dates: List[str]
    """The dates of the vintage series."""

    values: List[Optional[float]]
    """The values of the vintage series. Missing values are represented by null."""

    def __init__(self, vintage_values: VintageValuesResponse) -> None:
        self.vintage_time_stamp = vintage_values.get("vintageTimeStamp")
        self.dates = list(map(parser.parse, vintage_values["dates"]))
        self.values = list(
            map(
                lambda x: float(x) if x else None,
                vintage_values["values"],
            )
        )

    def __repr__(self):
        return f"VintageValues vintage_time_stamp: {self.vintage_time_stamp}"


class SeriesWithVintages:
    """A time series with times of change"""

    __slots__ = ("error_text", "error_code", "metadata", "vintages")

    error_text: Optional[str]
    """The error text if there was an error or not specified if there was no error"""

    error_code: Optional[int]
    """
    Set if there was an error and not specified if there was no error

    206 = PartialContent (The item was not modified and is not included in the response)
    304 = NotModified (The item was not modified and is not included in the response)
    403 = Forbidden (Access to the item was denied)
    404 = NotFound (The item was not found)
    500 = Other (There was an error and it is described in the error text)
    """

    metadata: Optional[Dict[str, Any]]
    """
    The time when this version of the series was recorded
    """

    vintages: List[VintageValues]
    """
    If specified, incremental updates can be return. PartialContent (206) will be returned in 
    that case. 
    The value should be from the metadata LastRevisionAdjustmentTimeStamp of the previous response.
    """

    def __init__(self, response: SeriesWithVintagesResponse) -> None:
        self.error_text = response.get("errorText")
        self.error_code = response.get("errorCode")
        self.metadata = response.get("metadata")
        vintages = response.get("vintages")
        self.vintages = list(map(VintageValues, vintages)) if vintages else []

    def __repr__(self):
        return f"SeriesWithVintages error_text: {self.error_text}, error_code: {self.error_code}"
