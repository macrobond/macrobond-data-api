from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(init=False)
class RevisionHistoryRequest:
    """Request of new revisions of a time series"""

    __slots__ = ("name", "if_modified_since", "last_revision", "last_revision_adjustment")

    name: str
    """The name of the series"""

    if_modified_since: Optional[datetime]
    """
    If specified, the series will only be returned if modified since the specified time. If not,
    NotModified (304) will be returned. The value should be from the metadata LastModifiedTimeStamp
    of the previous response.
    """

    last_revision: Optional[datetime]
    """
    If specified, incremental updates can be return.
    PartialContent (206) will be returned in that case. The value should be from the metadata
    LastRevisionTimeStamp of the previous response.
    """

    last_revision_adjustment: Optional[datetime]
    """
    If specified, incremental updates can be return. PartialContent (206) will be returned in 
    that case. 
    The value should be from the metadata LastRevisionAdjustmentTimeStamp of the previous response.
    """

    def __init__(
        self,
        name: str,
        if_modified_since: Optional[datetime] = None,
        last_revision: Optional[datetime] = None,
        last_revision_adjustment: Optional[datetime] = None,
    ) -> None:
        self.name = name
        self.if_modified_since = if_modified_since
        self.last_revision = last_revision
        self.last_revision_adjustment = last_revision_adjustment
