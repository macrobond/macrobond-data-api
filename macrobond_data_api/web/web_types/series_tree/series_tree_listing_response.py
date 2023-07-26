from typing import Optional, List, Dict, TypedDict


class SeriesTreeListingSeries(TypedDict):
    """Defines an aspect in a structured series list"""

    discontinued: Optional[bool]
    """
    If True then the series is discontinued.
    This is typically indicated by drawing the series title in red.
    """

    Indentation: Optional[int]
    """The indentation level."""

    emphasized: Optional[bool]
    """
    If True then the series is emphasized.
    This is typically indicated by drawing the series title in bold.
    """

    spaceAbove: Optional[bool]
    """If True then some extra space should be drawn above this series."""

    properties: Dict[str, object]
    """
    Properties that can be used for display purposes. It will always contain a property
    called Description. If there is a series,
    the property Name will contain the series name.
    If there is no Name, the series is missing and the description is typically shown as 'disabled'.
    """


class SeriesTreeListingGroup(TypedDict):
    """Defines an aspect in a structured series list"""

    title: Optional[str]
    """The title of the group. This is might be omitted if there is only one group."""

    series: List[SeriesTreeListingSeries]
    """The list of series in this group."""


class SeriesTreeListingAspect(TypedDict):
    """Defines an aspect in a structured series list"""

    title: Optional[str]
    """The title of the aspect. This is might be omitted if there is only one aspect."""

    description: Optional[str]
    """
    A longer description of the aspect that can be used as a tooltip.
    This is might be omitted if there is only one aspect.
    """

    groups: List[SeriesTreeListingGroup]


class SeriesTreeListingResponse(TypedDict):
    """A structured list of series for a leaf in the series database tree"""

    commonTitle: str
    """The common part of the series titles"""

    hasAspects: bool
    """If True then there are several aspects of the series which is typically displayed as tabs"""

    hasGroups: bool
    """If True then the list is grouped"""

    aspects: List[SeriesTreeListingAspect]
    """The list of aspects. There will always be at least one."""
