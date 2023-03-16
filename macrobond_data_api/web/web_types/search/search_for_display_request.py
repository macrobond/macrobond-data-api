from typing import Optional, List

from .search_request_base import SearchRequestBase


class SearchForDisplayRequest(SearchRequestBase):
    """Information about a search request with metadata as presentable text"""

    attributesForDisplayFormat: Optional[List[str]]
    """Attributes to return that will be formatted for as presentable text."""
