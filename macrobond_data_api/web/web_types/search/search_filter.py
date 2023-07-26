from typing import Optional, List, Dict, TypedDict


class SearchFilter(TypedDict, total=False):
    """A filter in a search request"""

    entityTypes: Optional[List[str]]
    """
    One or more entity types to include in the search. An empty list will include all types.
    If not specified, the search will be made for TimeSeries.
    """

    mustHaveValues: Optional[Dict[str, object]]
    """Pairs of attributes and values to be matched against entities when searching"""

    mustNotHaveValues: Optional[Dict[str, object]]
    """Pairs of attributes and values to exclude entities when searching"""

    mustHaveAttributes: Optional[List[str]]
    """Attributes to be matched against entities when searching. Any value will match."""

    mustNotHaveAttributes: Optional[List[str]]
    """Attributes to exclude entities when searching. Any value will match."""

    text: Optional[str]
    """Words to search for separated by space."""

    mustHaveFilterListPath: Optional[str]
    """
    Optional path to filter list that is added to the set of MustHaveValues.
    The paths are typically obtained from a call ListFilterLists.
    """
