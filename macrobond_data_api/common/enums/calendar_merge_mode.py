# pylint: disable=invalid-name , missing-module-docstring

from enum import IntEnum


class CalendarMergeMode(IntEnum):
    """Calendar merge modes."""

    FULL_CALENDAR = 0
    """ Include the full range."""

    AVAILABLE_IN_ALL = 1
    """Use points in time that are available in all calendars."""

    AVAILABLE_IN_ANY = 2
    """Use points in time that are available in any calendar."""
