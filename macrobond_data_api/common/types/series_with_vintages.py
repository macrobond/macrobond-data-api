from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from macrobond_data_api.common.enums import StatusCode

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


@dataclass(init=False)
class SeriesWithVintages:
    """A time series with times of change"""

    __slots__ = ("error_text", "status_code", "metadata", "vintages")

    error_text: Optional[str]
    """The error text if there was an error or not specified if there was no error"""

    status_code: StatusCode
    """
    Set if there was an error and not specified if there was no error
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
        status_code: StatusCode,
        metadata: Optional[Metadata],
        vintages: List[VintageValues],
    ) -> None:
        self.error_text = error_text
        self.status_code = status_code
        self.metadata = metadata
        self.vintages = vintages
