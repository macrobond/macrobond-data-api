# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, MutableMapping, TYPE_CHECKING
from typing_extensions import Literal

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import Series, DataFrame  # type: ignore


EntityColumnsLiterals = Literal["ErrorMessage", "Name", "PrimName", "FullDescription", "EntityType"]

EntityColumns = List[EntityColumnsLiterals]


class Entity:
    """
    Represents a Macrobond entity.
    """

    __slots__ = ("name", "error_message", "metadata")

    name: str
    error_message: str
    metadata: MutableMapping[str, Any]

    @property
    def is_error(self) -> bool:
        """
        True if there was an error downloading this entity. `Entity.error_message` will
        contain any error message.
        """
        return self.error_message != ""

    @property
    def primary_name(self) -> str:
        """
        The primary name of the entity.
        This can be different from the name requested if an alias was used in the request.
        """
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
        """
        The type of the entity.
        Common types are TimeSeries, Region, Release and Source.
        """
        entity_type = self.metadata["EntityType"]
        if isinstance(entity_type, list):
            entity_type = entity_type[0]
        return entity_type

    @property
    def is_discontinued(self) -> bool:
        """Returns True if the entity is discontinued and no longer updated."""
        entity_state = self.metadata.get("EntityState")
        return entity_state is not None and entity_state != 0

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        metadata: Optional[MutableMapping[str, Any]],
    ) -> None:
        self.name = name
        """The name of the entity."""

        self.error_message = error_message if error_message else ""
        """Contains an error message if `Entity.is_error` is True."""

        self.metadata = metadata if metadata else {}
        """The metadata of the entity."""

    def _add_metadata(self, destination: Dict[str, Any]) -> None:
        for key in self.metadata.keys():
            destination["metadata." + key] = self.metadata[key]

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary containing all the metadata."""
        if self.is_error:
            return {
                "Name": self.name,
                "ErrorMessage": self.error_message,
            }

        ret = {"Name": self.name}
        self._add_metadata(ret)
        return ret

    def metadata_to_pd_series(self, name: str = None) -> "Series":
        """Returns a Pandas series containing all the metadata."""
        pandas = _get_pandas()
        name = name if name else self.name
        return pandas.Series(self.metadata.values(), self.metadata.keys(), name=name)

    def __repr__(self):
        if self.is_error:
            return f"{self.__class__.__name__} with error, error message: {self.error_message}"
        return f"{self.__class__.__name__} PrimName: {self.primary_name}"

    def __bool__(self):
        return not self.is_error

    def __eq__(self, other):
        return self is other or (
            isinstance(other, Entity)
            and self.error_message == other.error_message
            and self.metadata == other.metadata
        )

    def __hash__(self):
        return hash(
            (
                self.error_message,
                self.metadata,
            )
        )
