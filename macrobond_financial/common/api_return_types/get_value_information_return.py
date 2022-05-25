# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Union, overload, List, Tuple, TYPE_CHECKING
from typing_extensions import Literal

from ..types import (
    MetadataValueInformationItem,
    TypedDictMetadataValueInformation,
    MetadataValueInformationColumns,
)

from .._get_pandas import _get_pandas


if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

SeriesValuesAndDatesColumns = List[Literal["Values", "Dates"]]


class GetValueInformationReturn(ABC):
    def __init__(self, name_val: Tuple[Tuple[str, str], ...]) -> None:
        self._name_val = name_val

    @abstractmethod
    def object(self) -> List[MetadataValueInformationItem]:
        ...

    def dict(self) -> List[TypedDictMetadataValueInformation]:
        return list(map(lambda x: x.to_dict(), self.object()))

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
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.dict()
        return pandas.DataFrame(*args, **kwargs)
