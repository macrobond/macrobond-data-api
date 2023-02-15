# pylint: disable=invalid-name , missing-module-docstring

from enum import IntEnum


class SeriesWeekdays(IntEnum):
    """A bitmask for the weekday used in a Macrobond daily time series."""

    SUNDAY = 1 << 0
    """Sunday."""

    MONDAY = 1 << 1
    """Monday."""

    TUESDAY = 1 << 2
    """Tuesday."""

    WEDNESDAY = 1 << 3
    """Wednesday."""

    THURSDAY = 1 << 4
    """Thursday."""

    FRIDAY = 1 << 5
    """Friday."""

    SATURDAY = 1 << 6
    """Saturday."""

    FULL_WEEK = MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY | SATURDAY | SUNDAY
    """All days of the week."""

    MONDAY_TO_FRIDAY = MONDAY | TUESDAY | WEDNESDAY | THURSDAY | FRIDAY
    """Standard five day week."""

    SATURDAY_TO_THURSDAY = MONDAY | TUESDAY | WEDNESDAY | THURSDAY | SATURDAY | SUNDAY
    """Saturday to Thursday, weekend on Friday."""

    SATURDAY_TO_WEDNESDAY = SATURDAY | SUNDAY | MONDAY | TUESDAY | WEDNESDAY
    """Saturday to Wednesday daymask, weekend on Thursday and Friday."""

    SUNDAY_TO_THURSDAY = SUNDAY | MONDAY | TUESDAY | WEDNESDAY | THURSDAY
    """Sunday to Thursday daymask, weekend on Friday and Saturday."""

    MONDAY_TO_THURSDAY_AND_SATURDAY = SATURDAY | MONDAY | TUESDAY | WEDNESDAY | THURSDAY
    """Monday to Thursday and Saturday, weekend on Friday and Sunday."""
