# -*- coding: utf-8 -*-

from typing import Any, Dict, Union, overload, List, TYPE_CHECKING, Tuple
from abc import ABC, abstractmethod

from ..types import Entity, EntityColumns, GetEntitiesError
from .._get_pandas import _get_pandas


if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetEntitiesReturn(ABC):
    def __init__(self, entity_names: Tuple[str, ...], _raise: bool) -> None:
        self._entity_names = entity_names
        self._raise = _raise

    @abstractmethod
    def _list_of_objects(self) -> List[Entity]:
        ...

    def list_of_objects(self) -> List[Entity]:
        entitys = self._list_of_objects()
        GetEntitiesError.raise_if(
            self._raise,
            map(
                lambda x, y: (x, y.error_message if y.is_error else None),
                self._entity_names,
                entitys,
            ),
        )
        return entitys

    def list_of_dicts(self) -> List[Dict[str, Any]]:
        return list(map(lambda x: x.to_dict(), self.list_of_objects()))

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
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)
