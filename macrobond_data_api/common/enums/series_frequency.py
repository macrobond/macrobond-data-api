# pylint: disable=invalid-name , missing-module-docstring

from enum import IntEnum


class SeriesFrequency(IntEnum):
    """The series frequency. This must match SeriesCalendarFrequency."""

    ANNUAL = 1
    """Once a year."""

    SEMIANNUAL = 2
    """Once in half a year."""

    QUADMONTHLY = 3
    """Once in 4 months."""

    QUARTERLY = 4
    """Once a quarter."""

    BIMONTHLY = 5
    """Once every 2 months."""

    MONTHLY = 6
    """Once a month."""

    WEEKLY = 7
    """Once a week."""

    DAILY = 8
    """Once a day."""

    LOWEST = 100
    """The lowest frequency."""

    HIGHEST = 101
    """The highest frequency."""
