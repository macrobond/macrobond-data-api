from dataclasses import dataclass
from typing import (
    Any,
    Optional,
    List,
    TYPE_CHECKING,
    Sequence,
    overload,
)
from typing_extensions import TypedDict, Literal

__pdoc__ = {
    "TypedDictMetadataValueInformationItem.__init__": False,
    "MetadataValueInformationItem.__init__": False,
    "MetadataValueInformation.__init__": False,
}

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore

MetadataValueInformationColumns = List[Literal["attribute_name", "value", "description", "comment"]]


class TypedDictMetadataValueInformationItem(TypedDict):
    """
    Contains information about one metadata attribute value.
    """

    attribute_name: str
    """The name of the metadata attribute"""

    value: Any
    """The value"""

    description: str
    """The description of the metadata value"""

    comment: Optional[str]
    """The comment of the metadata value"""


@dataclass(init=False)
class MetadataValueInformationItem:
    """
    Contains information about one metadata attribute value.
    """

    __slots__ = ("attribute_name", "value", "description", "comment")

    attribute_name: str
    value: Any
    description: str
    comment: Optional[str]

    def __init__(self, attribute_name: str, value: Any, description: str, comment: Optional[str]) -> None:
        self.attribute_name = attribute_name
        """The name of the metadata attribute"""

        self.value = value
        """The value"""

        self.description = description
        """The description of the metadata value"""

        self.comment = comment
        """The comment of the metadata value"""

    def to_pd_data_frame(self) -> "DataFrame":
        """The information represented as a Pandas DataFrame"""
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame([self.to_dict()])

    def to_dict(self) -> TypedDictMetadataValueInformationItem:
        """The information represented as a dictionary"""
        return {
            "attribute_name": self.attribute_name,
            "value": self.value,
            "description": self.description,
            "comment": self.comment,
        }

    def _repr_html_(self) -> str:
        return self.to_pd_data_frame()._repr_html_()


@dataclass(init=False)
class MetadataValueInformation(Sequence[MetadataValueInformationItem]):
    # fmt: off
    """
    The result of a call to `macrobond_data_api.common.api.Api.metadata_get_value_information`.  
    Contains information about the requested metadata attribute values.
    """
    # fmt: on

    __slots__ = ("attribute_name", "entities")

    entities: Sequence[MetadataValueInformationItem]
    attribute_name: str

    def __init__(
        self,
        entities: Sequence[MetadataValueInformationItem],
        attribute_name: str,
    ) -> None:
        super().__init__()
        self.entities = entities
        """entities"""
        self.attribute_name = attribute_name
        """The name of the metadata attribute"""

    def to_pd_data_frame(self) -> "DataFrame":
        """The information represented as a Pandas DataFrame"""
        import pandas  # pylint: disable=import-outside-toplevel

        return pandas.DataFrame(self.to_dict())

    def to_dict(self) -> List[TypedDictMetadataValueInformationItem]:
        """The information represented as a dictionary"""
        return list(map(lambda x: x.to_dict(), self))

    @overload
    def __getitem__(self, i: int) -> MetadataValueInformationItem:
        ...

    @overload
    def __getitem__(self, s: slice) -> List[MetadataValueInformationItem]:
        ...

    def __getitem__(self, key):  # type: ignore
        return self.entities[key]

    def __len__(self) -> int:
        return len(self.entities)

    def _repr_html_(self) -> str:
        frame = self.to_pd_data_frame()
        del frame["attribute_name"]
        return f"<h1>{self.attribute_name}</h1>" + frame._repr_html_()
