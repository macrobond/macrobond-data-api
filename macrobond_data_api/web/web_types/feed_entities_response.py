from typing import List, TypedDict


class EntityNameWithTimeStamp(TypedDict):
    """Name and timestamp of an entity"""

    name: str
    """The entity name"""

    modified: str
    """Timestamp when this entity was last modified"""


class FeedEntitiesResponse(TypedDict):
    """List of entities available in a feed"""

    timeStampForIfModifiedSince: str
    """
    A timestamp to pass as the ifModifiedSince parameter
    in the next request to get incremental updates.
    """

    downloadFullListOnOrAfter: str
    """
    Recommended earliest next time to request a full list 
    by omitting timeStampForIfModifiedSince.
    """

    state: int
    """
    The state of this list.

    0 = FullListing (A complete listing of all series. 
    Make another request for full data at some point after timestamp in downloadFullListOnOrAfter.)

    1 = UpToDate (The list contains all updates since the specified start date. 
    Wait 15 minutes before making another request where timeStampForIfModifiedSince is used.)

    2 = Incomplete (The list might not contain all updates.
    Wait one minute and then use the timeStampForIfModifiedSince in an a new request.)
    """

    entities: List["EntityNameWithTimeStamp"]
    """A list of entity names and timestamps when they were last modified."""
