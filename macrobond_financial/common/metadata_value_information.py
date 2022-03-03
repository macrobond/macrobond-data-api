# -*- coding: utf-8 -*-

from typing import Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover

    from typing_extensions import TypedDict, Literal

    MetadataValueInformationColumns = List[
        Literal["attribute_name", "value", "description", "comment"]
    ]

    class TypedDictMetadataValueInformation(TypedDict):

        attribute_name: str
        """The name of the metadata attribute"""

        value: Any
        """The value"""

        description: str
        """The description of the metadata value"""

        comment: Optional[str]
        """The comment of the metadata value"""


class MetadataValueInformation:
    """Information about a metadata value"""

    def __init__(
        self, attribute_name: str, value: Any, description: str, comment: Optional[str]
    ) -> None:
        self.attribute_name = attribute_name
        """The name of the metadata attribute"""

        self.value = value
        """The value"""

        self.description = description
        """The description of the metadata value"""

        self.comment = comment
        """The comment of the metadata value"""

    def __str__(self):
        return self.attribute_name

    def __repr__(self):
        return self.attribute_name

    def __eq__(self, other):
        if not isinstance(other, MetadataValueInformation):
            return NotImplemented

        return self is other or (
            self.attribute_name == other.attribute_name
            and self.value == other.value
            and self.description == other.description
            and self.comment == other.comment
        )

    def __hash__(self):
        return hash((self.attribute_name, self.value, self.description, self.comment))
