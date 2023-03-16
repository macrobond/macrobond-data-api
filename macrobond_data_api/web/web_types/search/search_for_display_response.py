from .search_response import SearchResponse


class SearchForDisplayResponse(SearchResponse):
    """Entity search response with metadata displayed for presentation purposes"""

    commonTitle: str
    """The common part of the title"""
