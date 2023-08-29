from typing import Optional, TypedDict


class RevisionHistoryRequest(TypedDict, total=False):
    """Request of new revisions of a time series"""

    name: str
    """The name of the series"""

    ifModifiedSince: Optional[str]
    """
    If specified, the series will only be returned if modified since the specified time. If not,
    NotModified (304) will be returned. The value should be from the metadata LastModifiedTimeStamp
    of the previous response.
    """

    lastRevision: Optional[str]
    """
    If specified, incremental updates can be return.
    PartialContent (206) will be returned in that case. The value should be from the metadata
    LastRevisionTimeStamp of the previous response.
    """

    lastRevisionAdjustment: Optional[str]
    """
    If specified, incremental updates can be return. PartialContent (206) will be returned in 
    that case. 
    The value should be from the metadata LastRevisionAdjustmentTimeStamp of the previous response.
    """
