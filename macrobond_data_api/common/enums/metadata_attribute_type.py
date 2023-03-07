from enum import IntEnum


class MetadataAttributeType(IntEnum):
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

    def __str__(self) -> str:
        if self.value == MetadataAttributeType.INT:
            return self.name + " (int)"
        if self.value == MetadataAttributeType.DOUBLE:
            return self.name + " (float)"
        if self.value == MetadataAttributeType.TIME_STAMP:
            return self.name + " (datetime)"
        if self.value == MetadataAttributeType.STRING:
            return self.name + " (str)"
        if self.value == MetadataAttributeType.BOOL:
            return self.name + " (bool)"

        return "Unknown"
