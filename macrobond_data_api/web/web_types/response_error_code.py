# pylint: disable=invalid-name , missing-module-docstring

from enum import IntEnum


class ResponseErrorCode(IntEnum):
    """Response Error Code"""

    PARTIAL_CONTENT = 206
    """The item was not modified and is not included in the response"""

    NOT_MODIFIED = 304
    """The item was not modified and is not included in the response"""

    NOT_FOUND = 404
    """The item was not found"""

    FORBIDDEN = 403
    """Access to the item was denied"""

    OTHER = 500
    """There was an error and it is described in the error text"""
