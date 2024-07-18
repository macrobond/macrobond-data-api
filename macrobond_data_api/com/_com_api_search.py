from datetime import datetime
from typing import List, TYPE_CHECKING

from macrobond_data_api.common.types import SearchResult
from ._fix_datetime import _fix_datetime


if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from macrobond_data_api.common.types import SearchFilter

    from .com_types import SearchQuery


def entity_search_multi_filter(
    self: "ComApi",
    *filters: "SearchFilter",
    include_discontinued: bool = False,
    no_metadata: bool = False  # pylint: disable=unused-argument
) -> SearchResult:
    querys: List["SearchQuery"] = []
    for _filter in filters:
        query = self.database.CreateSearchQuery()

        for entity_type in _filter.entity_types:
            query.SetEntityTypeFilter(entity_type)

        if _filter.text:
            query.Text = _filter.text

        for key in _filter.must_have_values:
            val = _filter.must_have_values[key]
            if isinstance(val, datetime):
                val = _fix_datetime(val)
            query.AddAttributeValueFilter(key, val)

        for key in _filter.must_not_have_values:
            val = _filter.must_not_have_values[key]
            if isinstance(val, datetime):
                val = _fix_datetime(val)
            query.AddAttributeValueFilter(key, _filter.must_not_have_values[key], False)

        for attribute in _filter.must_have_attributes:
            query.AddAttributeFilter(attribute)

        for attribute in _filter.must_not_have_attributes:
            query.AddAttributeFilter(attribute, False)

        query.IncludeDiscontinued = include_discontinued

        querys.append(query)

    result = self.database.Search(querys)
    return SearchResult([self._fill_metadata_from_entity(x) for x in result.Entities], result.IsTruncated)
