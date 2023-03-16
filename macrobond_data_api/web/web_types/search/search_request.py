from typing import Optional

from .search_request_base import SearchRequestBase


class SearchRequest(SearchRequestBase, total=False):
    """Information about a search request"""

    noMetadata: Optional[bool]
    """If set to false, no metadata but only the name of the entities will be returned."""

    allowLongResult: Optional[bool]
    """If set to true, allow for longer search results. noMetaData must be set to true."""
