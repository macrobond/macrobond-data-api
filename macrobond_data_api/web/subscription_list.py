# -*- coding: utf-8 -*-

from typing import Sequence, Optional, TYPE_CHECKING

from datetime import datetime

from dateutil import parser  # type: ignore

if TYPE_CHECKING:  # pragma: no cover
    from .web_types import FeedEntitiesResponse


class SubscriptionListItem:
    __slots__ = ("name", "modified")

    name: str
    """The entity name"""

    modified: datetime
    """Timestamp when this entity was last modified"""

    def __init__(self, name: str, modified: datetime) -> None:
        self.name = name
        self.modified = modified

    def __eq__(self, other):
        return self is other or (
            isinstance(other, SubscriptionListItem)
            and self.name == other.name
            and self.modified == other.modified
        )

    def __repr__(self):
        return f"SubscriptionListItem name: {self.name}, modified: {self.modified}"


class SubscriptionBody:
    __slots__ = ("time_stamp_for_if_modified_since", "download_full_list_on_or_after", "state")

    time_stamp_for_if_modified_since: datetime
    """
    A timestamp to pass as the ifModifiedSince parameter
    in the next request to get incremental updates.
    """

    download_full_list_on_or_after: Optional[datetime]
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

    def __init__(
        self,
        time_stamp_for_if_modified_since: datetime,
        download_full_list_on_or_after: Optional[datetime],
        state: int,
    ) -> None:
        self.time_stamp_for_if_modified_since = time_stamp_for_if_modified_since
        self.download_full_list_on_or_after = download_full_list_on_or_after
        self.state = state

    def __repr__(self):
        return "SubscriptionBody"


class SubscriptionList(Sequence[SubscriptionListItem], SubscriptionBody):
    __slots__ = ("items",)

    def __init__(self, response: "FeedEntitiesResponse") -> None:
        download_full = response.get("downloadFullListOnOrAfter")
        SubscriptionBody.__init__(
            self,
            parser.parse(response["timeStampForIfModifiedSince"]),
            parser.parse(download_full) if download_full is not None else None,
            response["state"],
        )
        self.items = list(
            map(
                lambda x: SubscriptionListItem(x["name"], parser.parse(x["modified"])),
                response["entities"],
            )
        )

    def __getitem__(self, index):
        return self.items.__getitem__(index)

    def __len__(self):
        return self.items.__len__()

    def __repr__(self):
        return "SubscriptionList"
