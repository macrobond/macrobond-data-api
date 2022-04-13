# -*- coding: utf-8 -*-

from typing import Union, overload, TYPE_CHECKING
from abc import ABC, abstractmethod

from ..typs import Entity, EntityColumns, EntityTypedDict

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetOneEntitieReturn(ABC):
    @abstractmethod
    def object(self) -> Entity:
        ...

    @abstractmethod
    def dict(self) -> EntityTypedDict:
        ...

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

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...

    @abstractmethod
    def metadata_as_data_frame(self) -> "DataFrame":
        ...

    # .from_dict(i['metadata'], orient='index')
