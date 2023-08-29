from typing import Optional, TypedDict


class StatusResponse(TypedDict):
    """A status response"""

    errorText: Optional[str]
    """The error text if there was an error or not specified if there was no error"""

    errorCode: Optional[int]
    """
    Set if there was an error and not specified if there was no error

    304 - The item was not modified and is not included in the response.
    404 - The item was not found.
    403 - Access to the item was denied.
    500 - There was an error and it is described in the error text.
    """
