from typing import List, Optional, TypedDict

from .metadata import MetadataAttributeTypeRestriction

from ...common.enums import MetadataAttributeType


class EntityInfoForDisplayItem(TypedDict):
    # pylint: disable = missing-class-docstring

    description: str
    """Description of the item"""

    comment: Optional[str]
    """The comment of the metadata value"""

    valueType: MetadataAttributeType
    """The value type of the metadata attribute"""

    valueRestriction: Optional[MetadataAttributeTypeRestriction]
    """Restriction on the value type"""

    value: object
    """The item value"""


class EntityInfoForDisplayGroup(TypedDict):
    # pylint: disable = missing-class-docstring

    description: str
    """Heading of the group"""

    title: Optional[str]
    """Title of the group"""

    items: List[EntityInfoForDisplayItem]
    """List of information items"""


class EntityInfoForDisplayResponse(TypedDict):
    """Entity search response with metadata displayed for presentation purposes"""

    groups: List["EntityInfoForDisplayGroup"]
    """A list of information groups"""
