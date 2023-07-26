from typing import Optional, Dict, Any, List, TypedDict

from .vintage_values_response import VintageValuesResponse


class SeriesWithVintagesResponse(TypedDict, total=False):
    """A time series with times of change"""

    errorText: Optional[str]
    """The error text if there was an error or not specified if there was no error"""

    errorCode: Optional[int]
    """
    Set if there was an error and not specified if there was no error

    206 = PartialContent (The item was not modified and is not included in the response)
    304 = NotModified (The item was not modified and is not included in the response)
    403 = Forbidden (Access to the item was denied)
    404 = NotFound (The item was not found)
    500 = Other (There was an error and it is described in the error text)
    """

    metadata: Optional[Dict[str, Any]]
    """
    The time when this version of the series was recorded
    """

    vintages: Optional[List[VintageValuesResponse]]
    """
    If specified, incremental updates can be return. PartialContent (206) will be returned in 
    that case. 
    The value should be from the metadata LastRevisionAdjustmentTimeStamp of the previous response.
    """
