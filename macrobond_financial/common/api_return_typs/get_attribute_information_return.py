# -*- coding: utf-8 -*-

"""module doc string"""

from typing import overload, Union, TYPE_CHECKING
from abc import ABC, abstractmethod

from ..typs import (
    MetadataAttributeInformation,
    TypedDictMetadataAttributeInformation,
    MetadataAttributeInformationColumns,
)

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetAttributeInformationReturn(ABC):
    @abstractmethod
    def object(self) -> MetadataAttributeInformation:
        ...

    @abstractmethod
    def dict(self) -> TypedDictMetadataAttributeInformation:
        ...

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[
            MetadataAttributeInformationColumns, "pandas_typing.Axes"
        ] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...
