from enum import IntEnum


class CalendarDateMode(IntEnum):
    """Calendar start/end date modes."""

    DATA_IN_ANY_SERIES = 0
    """All the series start or end when there is data in any series."""

    DATA_IN_ALL_SERIES = 1
    """All the series start or end when there is data in all series."""
