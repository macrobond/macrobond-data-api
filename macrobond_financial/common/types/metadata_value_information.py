# -*- coding: utf-8 -*-

from typing import (
    Any,
    Optional,
    List,
    TYPE_CHECKING,
    Sequence,
    Tuple,
    Union,
    overload,
    cast,
)
from typing_extensions import TypedDict, Literal

from .._get_pandas import _get_pandas


if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


MetadataValueInformationColumns = List[Literal["attribute_name", "value", "description", "comment"]]


class TypedDictMetadataValueInformation(TypedDict):

    attribute_name: str
    """The name of the metadata attribute"""

    value: Any
    """The value"""

    description: str
    """The description of the metadata value"""

    comment: Optional[str]
    """The comment of the metadata value"""


class MetadataValueInformationItem:
    """
    Contains information about one metadata attribute value.
    """
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

    def to_pd_data_frame(self) -> "DataFrame":
        """The information represented as a Pandas DataFrame"""
        pandas = _get_pandas()
        return pandas.DataFrame([self.to_dict()])

    def to_dict(self) -> TypedDictMetadataValueInformation:
        """The information represented as a dictionary"""
        return cast(TypedDictMetadataValueInformation, vars(self))

    def __str__(self):
        return (
            f"MetadataValueInformationItem attribute_name: {self.attribute_name},"
            + f" value: {self.value}, "
            + f" description: {self.description}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, MetadataValueInformationItem):
            return NotImplemented

        return self is other or (
            self.value == other.value
            and self.description == other.description
            and self.comment == other.comment
        )


class MetadataValueInformation(Sequence[MetadataValueInformationItem]):
    """
    The result of a call to `macrobond_financial.common.api.Api.metadata_get_value_information`.  
    Contains information about the requested metadata attribute values.
    """
    def __init__(
        self,
        attribute_name: str,
        items: Tuple[MetadataValueInformationItem, ...],
    ) -> None:
        self.attribute_name = attribute_name
        """The name of the metadata attribute"""

        self.items = items

    def to_pd_data_frame(self) -> "DataFrame":
        """The information represented as a Pandas DataFrame"""
        pandas = _get_pandas()
        return pandas.DataFrame(self.to_dict())

    def to_dict(self) -> List[TypedDictMetadataValueInformation]:
        """The information represented as a dictionary"""
        return list(map(lambda x: x.to_dict(), self.items))

    def __str__(self):
        return (
            f"MetadataValueInformation of {len(self)} items, attribute_name: {self.attribute_name}"
        )

    def __repr__(self):
        return str(self)

    @overload
    def __getitem__(self, idx: int) -> MetadataValueInformationItem:
        ...

    @overload
    def __getitem__(self, _slice: slice) -> Sequence[MetadataValueInformationItem]:
        ...

    def __getitem__(self, idx_or_slice: Union[int, slice]):
        return self.items.__getitem__(idx_or_slice)

    def __len__(self) -> int:
        return len(self.items)
