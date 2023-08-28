from typing import Optional, List, TypedDict
from enum import IntEnum

from ....common.enums import MetadataAttributeType


class MetadataAttributeTypeRestriction(IntEnum):
    URL = 1
    """The string is an URL"""

    EMAIL = 2
    """The string is an e-mail address"""

    DATE = 3
    """Only the date of the TimeStamp is valid"""

    POSITIVE = 4
    """The integer or double is >= 0"""

    JSON = 5
    """The string is encoded as JSON"""


class MetadataAttributeInformationResponse(TypedDict):
    """Information about a metadata attribute"""

    name: str
    """The name of the metadata attribute"""

    description: str
    """The description of the metadata attribute"""

    comment: Optional[str]
    """The comment of the metadata attribute"""

    valueType: MetadataAttributeType
    """The value type of the metadata attribute"""

    valueRestriction: Optional[MetadataAttributeTypeRestriction]
    """Restriction on the value type"""

    usesValueList: bool
    """If True, the metadata attribute uses a list of values"""

    canListValues: bool
    """
    If True then the values of this type of
    metadata can be listen using the ListAllValues function
    """

    canHaveMultipleValues: bool
    """If True then this type of metadata can have multiple values in a metadata collection"""

    isDatabaseEntity: bool
    """If True then this type of metadata is an entity that can be retrieved from the database"""

    appliesTo: Optional[List[str]]
    """If provided, specifies what types of entities that this attribute applies to"""
