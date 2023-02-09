from dataclasses import dataclass

from typing import Optional

from datetime import datetime

from .subscription_list_state import SubscriptionListState


@dataclass(init=False)
class SubscriptionBody:
    __slots__ = ("time_stamp_for_if_modified_since", "download_full_list_on_or_after", "state")

    time_stamp_for_if_modified_since: datetime
    download_full_list_on_or_after: Optional[datetime]
    state: SubscriptionListState

    def __init__(
        self,
        time_stamp_for_if_modified_since: datetime,
        download_full_list_on_or_after: Optional[datetime],
        state: SubscriptionListState,
    ) -> None:
        self.time_stamp_for_if_modified_since = time_stamp_for_if_modified_since
        """
        A timestamp to pass as the ifModifiedSince parameter
        in the next request to get incremental updates.
        """
        self.download_full_list_on_or_after = download_full_list_on_or_after
        """
        Recommended earliest next time to request a full list 
        by omitting timeStampForIfModifiedSince.
        """
        self.state = state
        """
        The state of this list.
        """
