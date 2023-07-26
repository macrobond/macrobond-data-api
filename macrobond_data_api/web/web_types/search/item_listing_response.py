from typing import Optional, List, TypedDict


class ItemInformation(TypedDict):
    # pylint: disable = missing-class-docstring

    title: str
    """The title of the item"""

    path: str
    """The path of the item"""


class ItemListingResponse(TypedDict):
    """The response of listing items that can be organized into directories"""

    title: str
    """The title of the directory"""

    directories: Optional[List["ItemListingResponse"]]
    """The list of sub directories if any."""

    items: Optional[List[ItemInformation]]
    """The list of if any."""
