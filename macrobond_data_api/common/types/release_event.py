from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from macrobond_data_api.common.enums import ReleaseEventItemKind

__pdoc__ = {
    "ReleaseEvent.__init__": False,
}


@dataclass(init=False)
class ReleaseEvent:
    """
    Represents a Macrobond release event.
    """

    __slots__ = ("expected_release_time", "source_release_time", "reference_period_date", "comment", "kind")

    expected_release_time: datetime
    source_release_time: datetime
    reference_period_date: Optional[datetime]
    comment: Optional[str]
    kind: ReleaseEventItemKind

    def __init__(
        self,
        expected_release_time: datetime,
        source_release_time: datetime,
        reference_period_date: Optional[datetime],
        comment: Optional[str],
        kind: ReleaseEventItemKind,
    ):
        self.expected_release_time = expected_release_time
        """The time when Macrobond expects the next update. This takes known delays and other factors into account."""

        self.source_release_time = source_release_time
        """The time when the next update will be published according to the data source"""

        self.reference_period_date = reference_period_date
        """The reference period of the expected update"""

        self.comment = comment

        self.kind = kind
        """The kind of event this item represents"""
