# -*- coding: utf-8 -*-


from datetime import datetime
from typing import Tuple, TYPE_CHECKING, Optional

from typing_extensions import TypedDict

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


class RevisionInfoDict(TypedDict, total=False):
    name: str
    error_message: str
    stores_revisions: bool
    has_revisions: bool
    time_stamp_of_first_revision: Optional[datetime]
    time_stamp_of_last_revision: Optional[datetime]
    vintage_time_stamps: Tuple[datetime, ...]


class RevisionInfo:

    __slots__ = (
        "name",
        "error_message",
        "stores_revisions",
        "has_revisions",
        "time_stamp_of_first_revision",
        "time_stamp_of_last_revision",
        "vintage_time_stamps",
    )

    name: str
    error_message: str
    stores_revisions: bool
    has_revisions: bool
    time_stamp_of_first_revision: Optional[datetime]
    time_stamp_of_last_revision: Optional[datetime]
    vintage_time_stamps: Tuple[datetime, ...]

    def __init__(
        self,
        name: str,
        error_message: str,
        stores_revisions: bool,
        has_revisions: bool,
        time_stamp_of_first_revision: Optional[datetime],
        time_stamp_of_last_revision: Optional[datetime],
        vintage_time_stamps: Tuple[datetime, ...],
    ) -> None:
        self.name = name
        """name"""

        self.error_message = error_message
        """error_message"""

        self.stores_revisions = stores_revisions
        """stores_revisions"""

        self.has_revisions = has_revisions
        """has_revisions"""

        self.time_stamp_of_first_revision = time_stamp_of_first_revision
        """time_stamp_of_first_revision"""

        self.time_stamp_of_last_revision = time_stamp_of_last_revision
        """time_stamp_of_last_revision"""

        self.vintage_time_stamps = vintage_time_stamps
        """vintage_time_stamps"""

    def to_dict(self) -> RevisionInfoDict:
        return {
            "name": self.name,
            "error_message": self.error_message,
            "stores_revisions": self.stores_revisions,
            "has_revisions": self.has_revisions,
            "time_stamp_of_first_revision": self.time_stamp_of_first_revision,
            "time_stamp_of_last_revision": self.time_stamp_of_last_revision,
            "vintage_time_stamps": self.vintage_time_stamps,
        }

    def to_pd_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()
        return pandas.DataFrame(self.to_dict())

    def __repr__(self):
        return f"RevisionInfo name: {self.name}"
