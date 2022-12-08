# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_data_api.common.types import SearchResult

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi
    from macrobond_data_api.common.types import SearchFilter

    from .web_types.search import SearchRequest, SearchFilter as WebSearchFilter

__pdoc__ = {
    "WebApi.__init__": False,
}


def entity_search_multi_filter(
    self: "WebApi",
    *filters: "SearchFilter",
    include_discontinued: bool = False,
    no_metadata: bool = False
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
        "noMetadata": no_metadata,
    }

    response = self.session.search.post_entities(request)

    results = list(
        map(self.session._create_metadata, response["results"])  # pylint: disable=protected-access
    )

    return SearchResult(results, response.get("isTruncated") is True)
