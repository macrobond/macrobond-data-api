from typing import Optional, List, TypedDict

from .search_filter import SearchFilter


class SearchRequestBase(TypedDict, total=False):
    includeDiscontinued: bool
    """If True, discontinued entities will be included in the search"""

    filters: Optional[List[SearchFilter]]
    """One or more filters that specifies what to search for"""
