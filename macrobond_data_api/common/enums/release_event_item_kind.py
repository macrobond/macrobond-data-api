from enum import IntEnum


class ReleaseEventItemKind(IntEnum):
    """What kind of release that values represents."""

    UNKNOWN = 0
    """Unknown"""

    REVISED = 1
    """Revised values"""

    NEW = 2
    """New values"""
