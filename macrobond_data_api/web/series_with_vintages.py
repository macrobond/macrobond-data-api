from datetime import datetime
from typing import Optional, List

from enum import IntFlag

from dateutil import parser

from macrobond_data_api.common.types.metadata import Metadata
from .web_types import VintageValuesResponse, SeriesWithVintagesResponse


__pdoc__ = {
    "VintageValues.__init__": False,
    "SeriesWithVintages.__init__": False,
}


class VintageValues:
    """A time series with times of change"""

    __slots__ = ("vintage_time_stamp", "dates", "values")

    vintage_time_stamp: Optional[datetime]
    """The time when this version of the series was recorded"""

    dates: List[datetime]
    """The dates of the vintage series."""

    values: List[Optional[float]]
    """The values of the vintage series. Missing values are represented by null."""

    def __init__(self, vintage_values: VintageValuesResponse) -> None:
        vintage_time_stamp = vintage_values.get("vintageTimeStamp")
        if vintage_time_stamp:
            self.vintage_time_stamp = parser.parse(vintage_time_stamp)
        else:
            self.vintage_time_stamp = None

        self.dates = [datetime(int(x[0:4]), int(x[5:7]), int(x[8:10])) for x in vintage_values["dates"]]

        self.values = [float(x) if x else None for x in vintage_values["values"]]

    def __repr__(self) -> str:
        return f"VintageValues vintage_time_stamp: {self.vintage_time_stamp}"


class SeriesWithVintagesErrorCode(IntFlag):
    PARTIAL_CONTENT = 206
    """The item was not modified and is not included in the response"""

    NOT_MODIFIED = 304
    """The item was not modified and is not included in the response"""

    FORBIDDEN = 403
    """Access to the item was denied"""

    NOT_FOUND = 404
    """The item was not found"""

    OTHER = 500
    """There was an error and it is described in the error text"""


class SeriesWithVintages:
    """A time series with times of change"""

    __slots__ = ("error_text", "error_code", "metadata", "vintages")

    error_text: Optional[str]
    """The error text if there was an error or not specified if there was no error"""

    error_code: Optional[SeriesWithVintagesErrorCode]
    """
    Set if there was an error and not specified if there was no error

    206 = PartialContent (The item was not modified and is not included in the response)
    304 = NotModified (The item was not modified and is not included in the response)
    403 = Forbidden (Access to the item was denied)
    404 = NotFound (The item was not found)
    500 = Other (There was an error and it is described in the error text)
    """

    metadata: Optional[Metadata]
    """
    The time when this version of the series was recorded
    """

    vintages: List[VintageValues]
    """
    If specified, incremental updates can be return. PartialContent (206) will be returned in 
    that case. 
    The value should be from the metadata LastRevisionAdjustmentTimeStamp of the previous response.
    """

    @property
    def primary_name(self) -> str:
        """The primary name of the entity."""
        if self.metadata is None:
            return ""
        prim_name = self.metadata["PrimName"]
        if isinstance(prim_name, list):
            prim_name = prim_name[0]
        return prim_name

    @property
    def last_revision(self) -> Optional[datetime]:
        """
        The timestamp of the last revision to be used in the next call to
        `macrobond_data_api.web.web_api.WebApi.get_all_vintages_multiple_series`.
        """
        return (
            self.metadata["LastRevisionTimeStamp"]
            if self.metadata and "LastRevisionTimeStamp" in self.metadata
            else None
        )

    @property
    def last_revision_adjustment(self) -> Optional[datetime]:
        """
        The timestamp of the last revision adjustment to be used in the next call to
        `macrobond_data_api.web.web_api.WebApi.get_all_vintages_multiple_series`.
        """
        return (
            self.metadata["LastRevisionAdjustmentTimeStamp"]
            if self.metadata and "LastRevisionAdjustmentTimeStamp" in self.metadata
            else None
        )

    @property
    def last_modified(self) -> Optional[datetime]:
        """
        The timestamp of the last modification to be used in the next call to
        `macrobond_data_api.web.web_api.WebApi.get_all_vintages_multiple_series`.
        """
        return (
            self.metadata["LastModifiedTimeStamp"]
            if self.metadata and "LastModifiedTimeStamp" in self.metadata
            else None
        )

    def __init__(self, response: SeriesWithVintagesResponse, metadata: Optional[Metadata]) -> None:
        self.error_text = response.get("errorText")
        error_code = response.get("errorCode")
        self.error_code = SeriesWithVintagesErrorCode(error_code) if error_code else None
        self.metadata = metadata
        self.vintages = []
        vintages = response.get("vintages")
        self.vintages = [VintageValues(x) for x in vintages] if vintages else []

    def __repr__(self) -> str:
        return (
            f"SeriesWithVintages primary_name: {self.primary_name}, "
            + f"error_text: {self.error_text}, error_code: {self.error_code}, "
            + f"vintages: {len(self.vintages)}"
        )
