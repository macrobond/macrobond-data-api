# pylint: disable= missing-module-docstring

from enum import IntEnum


class SeriesToHigherFrequencyMethod(IntEnum):
    """Methods for converting to higer frequency."""

    AUTO = 0
    """Determine the method based on the series classification."""

    SAME = 1
    """
    Duplicate the lower frequency value for each of the higher frequency
    series positions.
    """

    DISTRIBUTE = 2
    """
    Distribute the lower frequency value into equal sized parts for each
    of the higher frequency series positions.
    """

    PERCENTAGE_CHANGE = 3
    """
    Distribute the percentage change so that the product of the higher frequency
    observations - 100, is the same.
    """

    LINEAR_INTERPOLATION = 4
    """
    Use a linear interpolation between each pair of lower frequency values
    to fill in each of the higher frequency values.
    """

    PULSE = 5
    """
    Sets the value for the first observation in the period range and the other
    values to "missing".
    """

    QUADRATIC_DISTRIBUTION = 6
    """
    Use a quadratic interpolation that optimize the area under the lower
    frequency values to fill in the higher frequency values.
    """

    CUBIC_INTERPOLATION = 7
    """
    Use a cubic interpolation that optimize the area under the lower
    frequency values to fill in the higher frequency values.
    """

    CONDITIONAL_PERCENTAGE_CHANGE = 8
    """
    Distribute the percentage change so that the product of the higher frequency
    observations - 100, is the same, but only if pp100 is set on the series.
    """
