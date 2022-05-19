# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Union, Optional, TYPE_CHECKING, overload
from typing_extensions import Literal

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


EntityColumnsLiterals = Literal[
    "ErrorMessage", "Name", "PrimName", "FullDescription", "EntityType"
]

EntityColumns = List[EntityColumnsLiterals]


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

    def _add_metadata(self, destination: Dict[str, Any]) -> None:
        for key in self.metadata.keys():
            destination["metadata." + key] = self.metadata[key]

    def to_dict(self) -> Dict[str, Any]:
        if self.is_error:
            return {
                "Name": self.name,
                "ErrorMessage": self.error_message,
            }

        ret = {"Name": self.name}
        self._add_metadata(ret)
        return ret

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[EntityColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.to_dict()]
        return pandas.DataFrame(*args, **kwargs)

    def get_metadata_as_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()
        return pandas.DataFrame.from_dict(
            self.metadata, orient="index", columns=["Attributes"]
        )

    def __str__(self):
        if self.is_error:
            return f"Entity with error, error message: {self.error_message}"
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
