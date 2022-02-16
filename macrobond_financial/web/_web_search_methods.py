# -*- coding: utf-8 -*-

# pylint : disable = missing-module-docstring

from typing import TYPE_CHECKING, Dict, Any

from macrobond_financial.common import SearchMethods as CommonSearchMethods, \
    Entity as CommonEntity, \
    SearchResult

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session
    from macrobond_financial.common import SearchFilter
    from .web_typs.search_filter import SearchFilter as WebSearchFilter
    from .web_typs.search_request import SearchRequest


class _Entity(CommonEntity):

    _metadata: Dict[str, Any]

    def __init__(self, metadata: Dict[str, Any]) -> None:
        super().__init__()
        self._metadata = metadata

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    @property
    def name(self) -> str:
        return self._metadata['Name']

    @property
    def primary_name(self) -> str:
        return self._metadata['PrimName']

    @property
    def is_error(self) -> bool:
        return False

    @property
    def error_message(self) -> str:
        return ""

    @property
    def title(self) -> str:
        return self._metadata['FullDescription']

    @property
    def entity_type(self) -> str:
        return self._metadata['EntityType']

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata


class _WebSearchMethods(CommonSearchMethods):

    def __init__(self, session: 'Session') -> None:
        super().__init__()
        self.__search = session.search

    def series_multi_filter(
        self,
        *filters: 'SearchFilter',
        include_discontinued: bool = None
    ) -> SearchResult:
        def convert_filter_to_web_filter(_filter: 'SearchFilter') -> 'WebSearchFilter':
            return {
                'text': _filter.text,
                'entityTypes': list(_filter.entity_types),
                'mustHaveValues': _filter.must_have_values,
                'mustNotHaveValues': _filter.must_not_have_values,
                'mustHaveAttributes': list(_filter.must_have_attributes),
                'mustNotHaveAttributes': list(_filter.must_not_have_attributes),
            }
        web_filters = list(map(convert_filter_to_web_filter, filters))

        request: 'SearchRequest' = {'filters': web_filters}
        if include_discontinued is not None:
            request['includeDiscontinued'] = include_discontinued

        response = self.__search.post_entities(request)

        return SearchResult(
            list(map(_Entity, response['results'])),
            response.get('isTruncated') is True
        )
