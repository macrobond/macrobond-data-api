# pylint: disable= missing-module-docstring

from enum import IntEnum


class SeriesPartialPeriodsMethod(IntEnum):
    """Type of partial period method when converting to lower frequency."""

    NONE = 0
    """Do not include partial periods."""

    AUTO = 1
    """Determine the method based on the series meta data."""

    REPEAT_LAST_VALUE = 2
    """Fill up the partial period by repeating the last value."""

    FLOW_CURRENT_SUM = 3
    """Fill up the partial period with the average of the incomplete period."""

    PAST_RATE_OF_CHANGE = 4
    """Use the rate of change from the previous year to extend the partial period."""

    ZERO = 5
    """Fill up the partial period with zeroes."""
