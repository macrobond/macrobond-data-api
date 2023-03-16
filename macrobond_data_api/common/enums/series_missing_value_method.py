from enum import IntEnum


class SeriesMissingValueMethod(IntEnum):
    """Missing value methods."""

    NONE = 0
    """Do not fill in missing values."""

    AUTO = 1
    """Determine the method based on the series classification."""

    PREVIOUS_VALUE = 2
    """Use the previous non-missing value."""

    ZERO_VALUE = 3
    """Use the value zero."""

    LINEAR_INTERPOLATION = 4
    """Do a linear interpolation."""
