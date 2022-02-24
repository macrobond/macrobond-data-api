# -*- coding: utf-8 -*-

from typing import Any, Dict, List, TYPE_CHECKING

from macrobond_financial.common import SearchMethods as CommonSearchMethods, SearchResult

if TYPE_CHECKING:  # pragma: no cover
    from .com_typs import Connection, SearchQuery
    from macrobond_financial.common import SearchFilter


class _ComSearchMethods(CommonSearchMethods):

    def __init__(self, connection: 'Connection') -> None:
        super().__init__()
        self.__database = connection.Database

    def series_multi_filter(
        self,
        *filters: 'SearchFilter',
        include_discontinued: bool = None
    ) -> SearchResult:
        querys: List['SearchQuery'] = []
        for _filter in filters:
            query = self.__database.CreateSearchQuery()

            for entity_type in _filter.entity_types:
                query.SetEntityTypeFilter(entity_type)

            if _filter.text is not None:
                query.Text = _filter.text

            for key in _filter.must_have_values:
                query.AddAttributeValueFilter(key, _filter.must_have_values[key])

            for key in _filter.must_not_have_values:
                query.AddAttributeValueFilter(key, _filter.must_not_have_values[key], False)

            for attribute in _filter.must_have_attributes:
                query.AddAttributeFilter(attribute)

            for attribute in _filter.must_not_have_attributes:
                query.AddAttributeFilter(attribute, False)

            if include_discontinued is not None:
                query.IncludeDiscontinued = include_discontinued

            querys.append(query)

        result = self.__database.Search(querys)

        entities: List[Dict[str, Any]] = []

        for entitie in result.Entities:
            metadata: Dict[str, Any] = {}
            com_metadata = entitie.Metadata
            for names_and_description in com_metadata.ListNames():
                name = names_and_description[0]
                values = com_metadata.GetValues(name)
                if len(values) == 1:
                    metadata[name] = values[0]
                else:
                    metadata[name] = list(values)
            entities.append(metadata)

        return SearchResult(tuple(entities), result.IsTruncated)
