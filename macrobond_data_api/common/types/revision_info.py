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
    """Information about revisions of a time series."""

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
        """The name of the series"""

        self.error_message = error_message
        """Contains an error message in case of an error."""

        self.stores_revisions = stores_revisions
        """Returns True if revision history is stored for this series."""

        self.has_revisions = has_revisions
        """Returns True if any revisions have been stored for this series."""

        self.time_stamp_of_first_revision = time_stamp_of_first_revision
        """The timestamp of the first stored revision."""

        self.time_stamp_of_last_revision = time_stamp_of_last_revision
        """The timestamps of the last strored revision."""

        self.vintage_time_stamps = vintage_time_stamps
        """
        A tuple with the timestams of all stored revisions in time order with the oldest first.
        """

    def to_dict(self) -> RevisionInfoDict:
        """Returns a dictionary with the information of the series revisions."""
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
        """Returns a Pandas dataframe with the information about the series revisions."""
        pandas = _get_pandas()
        return pandas.DataFrame(self.to_dict())

    def __repr__(self):
        return f"RevisionInfo name: {self.name}"
