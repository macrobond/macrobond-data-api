# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Union, TYPE_CHECKING

from ._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover

    from pandas import DataFrame  # type: ignore

    from typing_extensions import TypedDict, Literal

    EntityColumnsLiterals = Literal[
        "ErrorMessage", "Name", "PrimName", "FullDescription", "EntityType"
    ]

    EntityColumns = List[EntityColumnsLiterals]

    class ErrorEntityTypedDict(TypedDict):
        Name: str
        ErrorMessage: str

    class EntityTypedDict(TypedDict):
        Name: str
        PrimName: str
        FullDescription: str
        EntityType: str

    EntityTypedDicts = Union[EntityTypedDict, ErrorEntityTypedDict]


class Entity:
    """Interface for a database Macrobond entity."""

    @property
    def is_error(self) -> bool:
        return self.error_message != ""

    @property
    def primary_name(self) -> str:
        """The primary name of the entity."""
        prim_name = self.metadata["PrimName"]
        if isinstance(prim_name, list):
            prim_name = prim_name[0]
        return prim_name

    @property
    def name(self) -> str:
        """The name of the entity."""
        name = self.metadata["Name"]
        if isinstance(name, list):
            name = name[0]
        return name

    @property
    def title(self) -> str:
        """The title of the entity."""
        full_description = self.metadata["FullDescription"]
        if isinstance(full_description, list):
            full_description = full_description[0]
        return full_description

    @property
    def entity_type(self) -> str:
        """The type of the entity."""
        entity_type = self.metadata["EntityType"]
        if isinstance(entity_type, list):
            entity_type = entity_type[0]
        return entity_type

    def __init__(self, error_message: str, metadata: Dict[str, Any]) -> None:
        self.error_message = error_message
        self.metadata = metadata

    def __str__(self):
        if self.is_error:
            return f"Entity with error, error message: {self.error_message}"

        # no name in meta data in web
        # name = self.metadata.get('Name') or ''
        # if isinstance(name, list):
        #     name = name[0]

        return f"{self.__class__.__name__}, PrimName: {self.primary_name}"

    def __repr__(self):
        return str(self)

    def get_metadata_as_data_frame(self) -> "DataFrame":
        metadata = self.metadata
        pandas = _get_pandas()
        return pandas.DataFrame.from_dict(
            metadata, orient="index", columns=["Attributes"]
        )
