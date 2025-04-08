from typing import Optional, TypedDict


class ReleaseEventItem(TypedDict):

    expectedReleaseTime: str
    """The time when Macrobond expects the next update. This takes known delays and other factors into account."""

    sourceReleaseTime: str
    """The time when the next update will be published according to the data source"""

    referencePeriodDate: Optional[str]
    """The reference period of the expected update"""

    comment: Optional[str]

    kind: int
    """The kind of event this item represents"""
