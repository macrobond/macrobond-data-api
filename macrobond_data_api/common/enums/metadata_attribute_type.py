# -*- coding: utf-8 -*-

from enum import IntFlag


class MetadataAttributeType(IntFlag):
    INT = 3
    """32-bit signed integer"""

    DOUBLE = 5
    """64-bit IEEE floating point number"""

    TIME_STAMP = 7
    """A time stamp including date, time of day and time zone"""

    STRING = 8
    """A unicode string"""

    BOOL = 11
    """A boolean value that can be true of false"""
