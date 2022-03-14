# -*- coding: utf-8 -*-

# pylint : disable = missing-module-docstring

from typing import TYPE_CHECKING

from macrobond_financial.common import (
    SearchMethods as CommonSearchMethods,
    SearchResult,
)

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session
    from macrobond_financial.common import SearchFilter
    from .web_typs.search_filter import SearchFilter as WebSearchFilter
    from .web_typs.search_request import SearchRequest


class _WebSearchMethods(CommonSearchMethods):
    def __init__(self, session: "Session") -> None:
        super().__init__()
        self.__search = session.search

    def series_multi_filter(
        self, *filters: "SearchFilter", include_discontinued: bool = False
    ) -> SearchResult:
        def convert_filter_to_web_filter(_filter: "SearchFilter") -> "WebSearchFilter":
            return {
                "text": _filter.text,
                "entityTypes": list(_filter.entity_types),
                "mustHaveValues": _filter.must_have_values,
                "mustNotHaveValues": _filter.must_not_have_values,
                "mustHaveAttributes": list(_filter.must_have_attributes),
                "mustNotHaveAttributes": list(_filter.must_not_have_attributes),
            }

        web_filters = list(map(convert_filter_to_web_filter, filters))

        request: "SearchRequest" = {
            "filters": web_filters,
            "includeDiscontinued": include_discontinued,
        }

        response = self.__search.post_entities(request)

        return SearchResult(
            tuple(response["results"]), response.get("isTruncated") is True
        )
