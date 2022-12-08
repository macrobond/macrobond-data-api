# -*- coding: utf-8 -*-

from typing import Any, Dict, List, TYPE_CHECKING

from macrobond_data_api.common.types import SearchResult

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from macrobond_data_api.common.types import SearchFilter

    from .com_types import SearchQuery

    from .com_types import Entity as ComEntity


def _fill_metadata_from_entity(com_entity: "ComEntity") -> Dict[str, Any]:
    ret = {}
    metadata = com_entity.Metadata

    for names_and_description in metadata.ListNames():
        name = names_and_description[0]
        values = metadata.GetValues(name)
        ret[name] = values[0] if len(values) == 1 else list(values)

    if "FullDescription" not in ret:
        ret["FullDescription"] = com_entity.Title

    return ret


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
            query.AddAttributeValueFilter(key, _filter.must_have_values[key])

        for key in _filter.must_not_have_values:
            query.AddAttributeValueFilter(key, _filter.must_not_have_values[key], False)

        for attribute in _filter.must_have_attributes:
            query.AddAttributeFilter(attribute)

        for attribute in _filter.must_not_have_attributes:
            query.AddAttributeFilter(attribute, False)

        query.IncludeDiscontinued = include_discontinued

        querys.append(query)

    result = self.database.Search(querys)

    entities = list(map(_fill_metadata_from_entity, result.Entities))
    return SearchResult(entities, result.IsTruncated)
