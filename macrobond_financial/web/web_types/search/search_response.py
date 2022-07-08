# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Any, Optional, List, Dict
from typing_extensions import TypedDict


class SearchResponse(TypedDict):
    """Entity search response"""

    isTruncated: Optional[bool]
    """If True, the search response is truncated"""

    results: List[Dict[str, Any]]
    """The matched entites"""
