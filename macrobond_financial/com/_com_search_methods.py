# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING

from macrobond_financial.common import (
    SearchMethods as CommonSearchMethods,
    SearchResult,
)

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from .com_typs import Connection, SearchQuery, Entity as ComEntity
    from macrobond_financial.common import SearchFilter


class _ComSearchMethods(CommonSearchMethods):
    def __init__(self, connection: "Connection") -> None:
        super().__init__()
        self.__database = connection.Database

    def series_multi_filter(
        self, *filters: "SearchFilter", include_discontinued: bool = False
    ) -> SearchResult:
        querys: List["SearchQuery"] = []
        for _filter in filters:
            query = self.__database.CreateSearchQuery()

            for entity_type in _filter.entity_types:
                query.SetEntityTypeFilter(entity_type)

            if _filter.text:
                query.Text = _filter.text

            for key in _filter.must_have_values:
                query.AddAttributeValueFilter(key, _filter.must_have_values[key])

            for key in _filter.must_not_have_values:
                query.AddAttributeValueFilter(
                    key, _filter.must_not_have_values[key], False
                )

            for attribute in _filter.must_have_attributes:
                query.AddAttributeFilter(attribute)

            for attribute in _filter.must_not_have_attributes:
                query.AddAttributeFilter(attribute, False)

            query.IncludeDiscontinued = include_discontinued

            querys.append(query)

        result = self.__database.Search(querys)

        entities = tuple(list(map(_fill_metadata_from_entity, result.Entities)))
        return SearchResult(entities, result.IsTruncated)
