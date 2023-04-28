from dataclasses import dataclass

from typing import Optional

from datetime import datetime

from .data_package_list_state import DataPackageListState


@dataclass(init=False)
class DataPackageBody:
    __slots__ = ("time_stamp_for_if_modified_since", "download_full_list_on_or_after", "state")

    time_stamp_for_if_modified_since: datetime
    download_full_list_on_or_after: Optional[datetime]
    state: DataPackageListState

    def __init__(
        self,
        time_stamp_for_if_modified_since: datetime,
        download_full_list_on_or_after: Optional[datetime],
        state: DataPackageListState,
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
