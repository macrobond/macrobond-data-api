# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Union, TYPE_CHECKING, List, overload, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:  # pragma: no cover
    from .series_methods import Entity


class SearchMethods(ABC):

    def search(
        self,
        text: str = None,
        entity_types: Union[Sequence[str], str] = None,
        must_have_values: Dict[str, object] = None,
        must_not_have_values: Dict[str, object] = None,
        must_have_attributes: Union[Sequence[str], str] = None,
        must_not_have_attributes: Union[Sequence[str], str] = None,
        include_discontinued: bool = None
    ) -> 'SearchResult':
        return self.series_multi_filter(
            SearchFilter(
                text=text,
                entity_types=entity_types,
                must_have_values=must_have_values,
                must_not_have_values=must_not_have_values,
                must_have_attributes=must_have_attributes,
                must_not_have_attributes=must_not_have_attributes,
            ),
            include_discontinued=include_discontinued
        )

    @abstractmethod
    def series_multi_filter(
        self,
        *filters: 'SearchFilter',
        include_discontinued: bool = None
    ) -> 'SearchResult':
        ...  # pragma: no cover


class SearchFilter:

    text: Optional[str]
    entity_types: Sequence[str]
    must_have_values: Dict[str, object]
    must_not_have_values: Dict[str, object]
    must_have_attributes: Sequence[str]
    must_not_have_attributes: Sequence[str]

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

        self.must_have_values = \
            must_have_values if must_have_values is not None else {}

        self.must_not_have_values = \
            must_not_have_values if must_not_have_values is not None else {}

        if isinstance(must_have_attributes, str):
            self.must_have_attributes: Sequence[str] = [must_have_attributes]
        else:
            self.must_have_attributes = must_have_attributes if \
                must_have_attributes is not None else []

        if isinstance(must_not_have_attributes, str):
            self.must_not_have_attributes: Sequence[str] = [must_not_have_attributes]
        else:
            self.must_not_have_attributes = \
                must_not_have_attributes if must_not_have_attributes is not None else []


class SearchResult(Sequence['Entity']):

    entities: List['Entity']

    is_truncated: bool

    def __init__(self, entities: List['Entity'], is_truncated: bool) -> None:
        self.entities = entities
        self.is_truncated = is_truncated

    def __str__(self):
        return f'SearchResult of {len(self)} entities, is is_truncated {self.is_truncated}'

    def __repr__(self):
        return str(self)

    @overload
    def __getitem__(self, idx: int) -> 'Entity':
        ...

    @overload
    def __getitem__(self, s: slice) -> Sequence['Entity']:
        ...

    def __getitem__(self, item: Union[int, slice]):
        return self.entities.__getitem__(item)

    def __len__(self) -> int:
        return len(self.entities)
