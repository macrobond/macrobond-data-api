# -*- coding: utf-8 -*-

from typing import Any, Dict, Union, overload, TYPE_CHECKING
from abc import ABC, abstractmethod

from ..typs import Entity, EntityColumns, GetEntitiesError

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetOneEntityReturn(ABC):
    def __init__(self, entity_name: str, _raise: bool) -> None:
        self._entity_name = entity_name
        self._raise = _raise

    @abstractmethod
    def _object(self) -> Entity:
        ...

    def object(self) -> Entity:
        entity = self._object()
        if self._raise and entity.is_error:
            raise GetEntitiesError(self._entity_name, entity.error_message)
        return entity

    def dict(self) -> Dict[str, Any]:
        return self.object().to_dict()

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
        return self.object().data_frame(*args, **kwargs)

    def metadata_as_data_frame(self) -> "DataFrame":
        return self.object().get_metadata_as_data_frame()
