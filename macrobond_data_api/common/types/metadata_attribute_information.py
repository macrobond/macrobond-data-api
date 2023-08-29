from dataclasses import dataclass

from typing import Optional, List, TYPE_CHECKING, Literal, TypedDict

__pdoc__ = {
    "MetadataAttributeInformation.__init__": False,
    "TypedDictMetadataAttributeInformation.__init__": False,
}

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame
    from ..enums import MetadataAttributeType

MetadataAttributeInformationColumns = List[
    Literal[
        "name",
        "description",
        "comment",
        "value_type",
        "uses_value_list",
        "can_list_values",
        "can_have_multiple_values",
        "is_database_entity",
    ]
]


class TypedDictMetadataAttributeInformation(TypedDict):
    # fmt: off
    """
    The result of a call to `macrobond_data_api.common.api.Api.metadata_get_attribute_information`.  
    Contains information about the requested metadata attributes.
    """
    # fmt: on

    name: str
    """The name of the metadata attribute"""

    description: str
    """The description of the metadata attribute"""

    comment: Optional[str]
    """The comment of the metadata attribute"""

    value_type: "MetadataAttributeType"
    """The value type of the metadata attribute"""

    uses_value_list: bool
    """If True, the metadata attribute uses a list of values"""

    can_list_values: bool
    """
    If True then the values of this type of metadata can be listed
    using the `macrobond_data_api.common.api.Api.metadata_list_values` function
    """

    can_have_multiple_values: bool
    """If True then this type of metadata can have multiple values in a metadata collection"""

    is_database_entity: bool
    """
    If True then this type of metadata is an entity that can be retrieved from the database using
    the `macrobond_data_api.common.api.Api.get_one_entity` function
    """


@dataclass(init=False)
class MetadataAttributeInformation:
    # fmt: off
    """
    The result of a call to `macrobond_data_api.common.api.Api.metadata_get_attribute_information`.  
    Contains information about the requested metadata attributes.
    """
    # fmt: on

    __slots__ = (
        "name",
        "description",
        "comment",
        "value_type",
        "uses_value_list",
        "can_list_values",
        "can_have_multiple_values",
        "is_database_entity",
    )

    name: str
    description: str
    comment: Optional[str]
    value_type: "MetadataAttributeType"
    uses_value_list: bool
    can_list_values: bool
    can_have_multiple_values: bool
    is_database_entity: bool

    def __init__(
        self,
        name: str,
        description: str,
        comment: Optional[str],
        value_type: "MetadataAttributeType",
        uses_value_list: bool,
        can_list_values: bool,
        can_have_multiple_values: bool,
        is_database_entity: bool,
    ) -> None:
        self.name = name
        """The name of the metadata attribute"""

        self.description = description
        """The description of the metadata attribute"""

        self.comment = comment
        """The comment of the metadata attribute"""

        self.value_type = value_type
        """The value type of the metadata attribute"""

        self.uses_value_list = uses_value_list
        """If True, the metadata attribute uses a list of values"""

        self.can_list_values = can_list_values
        """
        If True then the values of this type of
        metadata can be listed by calling `macrobond_data_api.common.api.Api.metadata_list_values`
        """

        self.can_have_multiple_values = can_have_multiple_values
        """If True then this type of metadata can have multiple values in a metadata collection"""

        self.is_database_entity = is_database_entity
        """
        If True then this type of metadata is an entity that can be retrieved from the database
        """

    def to_dict(self) -> TypedDictMetadataAttributeInformation:
        """The information represented as a dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "comment": self.comment,
            "value_type": self.value_type,
            "uses_value_list": self.uses_value_list,
            "can_list_values": self.can_list_values,
            "can_have_multiple_values": self.can_have_multiple_values,
            "is_database_entity": self.is_database_entity,
        }

    def to_pd_data_frame(self) -> "DataFrame":
        """The information represented as a Pandas DataFrame"""
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame([self.to_dict()], dtype="object")

    def _repr_html_(self) -> str:
        return self.to_pd_data_frame()._repr_html_()
