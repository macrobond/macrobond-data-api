from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from enum import IntEnum

from .metadata import Metadata

__pdoc__ = {
    "VintageValues.__init__": False,
    "SeriesWithVintages.__init__": False,
}


@dataclass(init=False)
class VintageValues:
    """A time series with times of change"""

    __slots__ = ("vintage_time_stamp", "dates", "values")

    vintage_time_stamp: Optional[datetime]
    """The time when this version of the series was recorded"""

    dates: List[datetime]
    """The dates of the vintage series."""

    values: List[Optional[float]]
    """The values of the vintage series. Missing values are represented by null."""

    def __init__(
        self, vintage_time_stamp: Optional[datetime], dates: List[datetime], values: List[Optional[float]]
    ) -> None:
        self.vintage_time_stamp = vintage_time_stamp
        self.dates = dates
        self.values = values


class SeriesWithVintagesErrorCode(IntEnum):
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


@dataclass(init=False)
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
        `macrobond_data_api.common.api.Api.get_many_series_with_revisions`.
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
        `macrobond_data_api.common.api.Api.get_many_series_with_revisions`.
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
        `macrobond_data_api.common.api.Api.get_many_series_with_revisions`.
        """
        return (
            self.metadata["LastModifiedTimeStamp"]
            if self.metadata and "LastModifiedTimeStamp" in self.metadata
            else None
        )

    def __init__(
        self,
        error_text: Optional[str],
        error_code: Optional[SeriesWithVintagesErrorCode],
        metadata: Optional[Metadata],
        vintages: List[VintageValues],
    ) -> None:
        self.error_text = error_text
        self.error_code = error_code
        self.metadata = metadata
        self.vintages = vintages
