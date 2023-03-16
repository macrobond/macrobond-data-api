from typing import Optional, List

from .entity_response import EntityResponse


class ValuesResponse(EntityResponse):
    """A series"""

    values: Optional[List[int]]
    """
    The values of the series or not specified if there was an error.
    Missing values are represented by null.
    """
