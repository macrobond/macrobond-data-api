# -*- coding: utf-8 -*-

from typing import Any, Dict, Sequence, Union, Tuple, overload, TYPE_CHECKING
from abc import ABC, abstractmethod

from macrobond_financial.common._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class SearchMethods(ABC):
    def search(
        self,
        text: str = None,
        entity_types: Union[Sequence[str], str] = None,
        must_have_values: Dict[str, object] = None,
        must_not_have_values: Dict[str, object] = None,
        must_have_attributes: Union[Sequence[str], str] = None,
        must_not_have_attributes: Union[Sequence[str], str] = None,
        include_discontinued: bool = None,
    ) -> "SearchResult":
        return self.series_multi_filter(
            SearchFilter(
                text=text,
                entity_types=entity_types,
                must_have_values=must_have_values,
                must_not_have_values=must_not_have_values,
                must_have_attributes=must_have_attributes,
                must_not_have_attributes=must_not_have_attributes,
            ),
            include_discontinued=include_discontinued,
        )

    @abstractmethod
    def series_multi_filter(
        self, *filters: "SearchFilter", include_discontinued: bool = None
    ) -> "SearchResult":
        ...  # pragma: no cover


class SearchFilter:
    def __init__(
        self,
        text: str = None,
        entity_types: Union[Sequence[str], str] = None,
        must_have_values: Dict[str, object] = None,
        must_not_have_values: Dict[str, object] = None,
        must_have_attributes: Union[Sequence[str], str] = None,
        must_not_have_attributes: Union[Sequence[str], str] = None,
    ) -> None:
        self.text = text

        if isinstance(entity_types, str):
            self.entity_types: Sequence[str] = [entity_types]
        else:
            self.entity_types = entity_types if entity_types is not None else []

        self.must_have_values: Dict[str, object] = (
            must_have_values if must_have_values is not None else {}
        )

        self.must_not_have_values: Dict[str, object] = (
            must_not_have_values if must_not_have_values is not None else {}
        )

        if isinstance(must_have_attributes, str):
            self.must_have_attributes: Sequence[str] = [must_have_attributes]
        else:
            self.must_have_attributes = (
                must_have_attributes if must_have_attributes is not None else []
            )

        if isinstance(must_not_have_attributes, str):
            self.must_not_have_attributes: Sequence[str] = [must_not_have_attributes]
        else:
            self.must_not_have_attributes = (
                must_not_have_attributes if must_not_have_attributes is not None else []
            )


class SearchResult(Sequence[Dict[str, Any]]):
    def __init__(
        self, entities: Tuple[Dict[str, Any], ...], is_truncated: bool
    ) -> None:
        self.entities = entities
        self.is_truncated = is_truncated

    def __str__(self):
        return (
            f"SearchResult of {len(self)} entities, is is_truncated {self.is_truncated}"
        )

    def __repr__(self):
        return str(self)

    @overload
    def __getitem__(self, idx: int) -> Dict[str, Any]:
        ...

    @overload
    def __getitem__(self, _slice: slice) -> Sequence[Dict[str, Any]]:
        ...

    def __getitem__(self, idx_or_slice: Union[int, slice]):
        return self.entities.__getitem__(idx_or_slice)

    def __len__(self) -> int:
        return len(self.entities)

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: "pandas_typing.Axes" = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.entities
        return pandas.DataFrame(*args, **kwargs)
