# -*- coding: utf-8 -*-

from typing import Optional

from datetime import datetime

from .subscription_list_state import SubscriptionListState


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

    state: SubscriptionListState
    """
    The state of this list.
    """

    def __init__(
        self,
        time_stamp_for_if_modified_since: datetime,
        download_full_list_on_or_after: Optional[datetime],
        state: SubscriptionListState,
    ) -> None:
        self.time_stamp_for_if_modified_since = time_stamp_for_if_modified_since
        self.download_full_list_on_or_after = download_full_list_on_or_after
        self.state = state

    def __repr__(self):
        return (
            f"SubscriptionBody {self.time_stamp_for_if_modified_since}"
            + f" {self.download_full_list_on_or_after} {self.state}"
        )
