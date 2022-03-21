# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from typing_extensions import TypedDict, Literal

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover

    from pandas import DataFrame  # type: ignore


EntityColumnsLiterals = Literal[
    "ErrorMessage", "Name", "PrimName", "FullDescription", "EntityType"
]

EntityColumns = List[EntityColumnsLiterals]


class EntityTypedDict(TypedDict, total=False):
    ErrorMessage: str
    Name: str
    MetaData: Dict[str, Any]


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

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        metadata: Optional[Dict[str, Any]],
    ) -> None:
        self.name = name
        self.error_message = error_message if error_message else ""
        self.metadata = metadata = metadata if metadata else {}

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

    def __bool__(self):
        return not self.is_error

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented

        return self is other or (
            self.error_message == other.error_message
            and self.metadata == other.metadata
        )

    def __hash__(self):
        return hash(
            (
                self.error_message,
                self.metadata,
            )
        )

    def get_metadata_as_data_frame(self) -> "DataFrame":
        metadata = self.metadata
        pandas = _get_pandas()
        return pandas.DataFrame.from_dict(
            metadata, orient="index", columns=["Attributes"]
        )
