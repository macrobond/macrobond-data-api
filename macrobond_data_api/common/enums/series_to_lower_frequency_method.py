# pylint: disable= missing-module-docstring

from enum import IntEnum


class SeriesToLowerFrequencyMethod(IntEnum):
    """Methods for converting to lower frequency."""

    AUTO = 0
    """Determine the method based on the series classification."""

    LAST = 1
    """Use last observation in higher frequency when converting to lower frequency."""

    FIRST = 2
    """Use first observation in higher frequency when converting to lower frequency."""

    FLOW = 3
    """Use aggregate of observations in higher frequency when converting to lower frequency."""

    PERCENTAGE_CHANGE = 4
    """Use recalculated percentage changes when converting pp100 series."""

    HIGHEST = 5
    """Use highest observation in higher frequency when converting to lower frequency."""

    LOWEST = 6
    """Use lowest observation in higher frequency when converting to lower frequency."""

    AVERAGE = 7
    """Use average of observations in higher frequency when converting to lower frequency."""

    CONDITIONAL_PERCENTAGE_CHANGE = 8
    """
    Use recalculated percentage changes when converting pp100 series,
    but only if it actually has the pp100 attribute.
    """
