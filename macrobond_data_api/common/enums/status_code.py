from enum import IntEnum


class StatusCode(IntEnum):
    """Status Code"""

    OK = 200
    """All is well"""

    PARTIAL_CONTENT = 206
    """This is an incremental update that includes only revisions added"""

    NOT_MODIFIED = 304
    """The item was not modified and is not included in the response"""

    FORBIDDEN = 403
    """Access to the item was denied"""

    NOT_FOUND = 404
    """The item was not found"""

    OTHER = 500
    """There was an error and it is described in the error text"""
