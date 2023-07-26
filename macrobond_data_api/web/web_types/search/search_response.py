from typing import Any, Optional, List, Dict, TypedDict


class SearchResponse(TypedDict):
    """Entity search response"""

    isTruncated: Optional[bool]
    """If True, the search response is truncated"""

    results: List[Dict[str, Any]]
    """The matched entites"""
