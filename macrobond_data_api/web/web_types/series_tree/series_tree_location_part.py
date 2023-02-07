# pylint: disable = missing-module-docstring

from typing import Optional
from typing_extensions import TypedDict


class SeriesTreeLocationPart(TypedDict):
    """A location in the database tree"""

    title: str
    """The title of the location element"""

    child: Optional["SeriesTreeLocationPart"]
    """The child of the location part"""
