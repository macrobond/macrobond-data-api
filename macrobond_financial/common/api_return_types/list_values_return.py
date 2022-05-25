# -*- coding: utf-8 -*-

from typing import List, overload, Union, TYPE_CHECKING
from abc import ABC, abstractmethod

from ..types import (
    MetadataValueInformation,
    TypedDictMetadataValueInformation,
    MetadataValueInformationColumns,
)

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class ListValuesReturn(ABC):
    @abstractmethod
    def object(self) -> MetadataValueInformation:
        ...

    def list_of_dicts(self) -> List[TypedDictMetadataValueInformation]:
        return self.object().to_dict()

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[MetadataValueInformationColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        return self.object().data_frame(*args, **kwargs)
