# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Optional
from enum import IntFlag
from typing_extensions import TypedDict


class ResponseErrorCode(IntFlag):
    """Response Error Codes"""

    NOT_MODIFIED = 304
    """The item was not modified and is not included in the response"""

    NOT_FOUND = 404
    """The item was not found"""

    FORBIDDEN = 403
    """Access to the item was denied"""

    OTHER = 500
    """There was an error and it is described in the error text"""


class StatusResponse(TypedDict):
    """A status response"""

    errorText: Optional[str]
    """The error text if there was an error or not specified if there was no error"""

    errorCode: Optional[ResponseErrorCode]
    """Set if there was an error and not specified if there was no error"""
