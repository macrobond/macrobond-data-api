# -*- coding: utf-8 -*-

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Callable, Sequence, Tuple

import ijson  # type: ignore
from dateutil import parser  # type: ignore

from macrobond_data_api.common import Api

from macrobond_data_api.common.types import SearchResultLong

from .series_with_vintages import SeriesWithVintages
from .subscription_list import (
    SubscriptionList,
    SubscriptionBody,
    SubscriptionListItem,
)

from ._web_api_metadata import (
    metadata_list_values,
    metadata_get_attribute_information,
    metadata_get_value_information,
)

from ._web_api_revision import (
    get_all_vintage_series,
    get_nth_release,
    get_revision_info,
    get_vintage_series,
    get_observation_history,
)

from ._web_api_series import (
    get_one_series,
    get_series,
    get_one_entity,
    get_entities,
    get_unified_series,
)

from ._web_api_search import entity_search_multi_filter

from .session import Session, _raise_on_error

if TYPE_CHECKING:  # pragma: no cover
    from .web_types import SeriesWithVintagesResponse, RevisionHistoryRequest

    from macrobond_data_api.common.types import SearchFilter

    from .web_types.search import SearchRequest, SearchFilter as WebSearchFilter


__pdoc__ = {
    "WebApi.__init__": False,
}


def _get_subscription_list_iterative_pars_body(
    ijson_parse,
) -> Tuple[Optional[datetime], Optional[datetime], Any]:
    time_stamp_for_if_modified_since: Optional[datetime] = None
    download_full_list_on_or_after: Optional[datetime] = None
    state = -1
    for prefix, event, value in ijson_parse:
        if prefix == "timeStampForIfModifiedSince":
            if event != "string":
                raise Exception("bad format: timeStampForIfModifiedSince is not a string")
            time_stamp_for_if_modified_since = parser.parse(value)
        elif prefix == "downloadFullListOnOrAfter":
            if event != "string":
                raise Exception("bad format: downloadFullListOnOrAfter is not a string")
            download_full_list_on_or_after = parser.parse(value)
        elif prefix == "state":
            if event != "number":
                raise Exception("bad format: state is not a number")
            state = value
        elif event == "start_array":
            if prefix != "entities":
                raise Exception("bad format: event start_array do not have a prefix of entities")
            break
    return time_stamp_for_if_modified_since, download_full_list_on_or_after, state


def _get_subscription_list_iterative_pars_items(
    ijson_parse, items_callback: Callable[[List[SubscriptionListItem]], Optional[bool]]
) -> None:
    name = ""
    modified: Optional[datetime] = None
    items: List[SubscriptionListItem] = []

    for prefix, event, value in ijson_parse:
        if event == "end_map":
            if name == "":
                raise Exception("bad format: name was not found")
            if modified is None:
                raise Exception("bad format: modified was not found")
            items.append(SubscriptionListItem(name, modified))
            name = ""
            modified = None
            if len(items) == 200:
                if items_callback(items) is False:
                    return
                items = []
        elif event == "end_array":
            break
        elif prefix == "entities.item.name":
            if event != "string":
                raise Exception("bad format: entities.item.name is not a string")
            name = value
        elif prefix == "entities.item.modified":
            if event != "string":
                raise Exception("bad format: entities.item.modified is not a string")
            modified = parser.parse(value)

    if len(items) != 0:
        items_callback(items)


class WebApi(Api):
    def __init__(self, session: Session) -> None:
        super().__init__()
        self.__session = session

    @property
    def session(self) -> Session:
        return self.__session

    # metadata

    metadata_list_values = metadata_list_values

    metadata_get_attribute_information = metadata_get_attribute_information

    metadata_get_value_information = metadata_get_value_information

    # revision

    get_revision_info = get_revision_info

    get_vintage_series = get_vintage_series

    get_nth_release = get_nth_release

    get_all_vintage_series = get_all_vintage_series

    get_observation_history = get_observation_history

    # web onley
    def get_subscription_list(self, if_modified_since: datetime = None) -> SubscriptionList:
        return SubscriptionList(self.session.series.get_subscription_list(if_modified_since))

    # web onley
    def get_subscription_list_iterative(
        self,
        body_callback: Callable[[SubscriptionBody], Optional[bool]],
        items_callback: Callable[[List[SubscriptionListItem]], Optional[bool]],
        if_modified_since: datetime = None,
    ) -> None:

        params = {}

        if if_modified_since:
            params["ifModifiedSince"] = if_modified_since.isoformat()

        with self.__session.get(
            "v1/series/getsubscriptionlist", params=params, stream=True
        ) as response:
            _raise_on_error(response)
            ijson_parse = ijson.parse(response.raw)

            (
                time_stamp_for_if_modified_since,
                download_full_list_on_or_after,
                state,
            ) = _get_subscription_list_iterative_pars_body(ijson_parse)

            if state == -1:
                raise Exception("bad format: state was not found")
            if time_stamp_for_if_modified_since is None:
                raise Exception("bad format: timeStampForIfModifiedSince was not found")
            if download_full_list_on_or_after is None:
                raise Exception("bad format: downloadFullListOnOrAfter was not found")

            if (
                body_callback(
                    SubscriptionBody(
                        time_stamp_for_if_modified_since, download_full_list_on_or_after, state
                    )
                )
                is False
            ):
                return

            _get_subscription_list_iterative_pars_items(ijson_parse, items_callback)

    def get_fetch_all_vintageseries(
        self,
        callback: Callable[[SeriesWithVintages], None],
        requests: Sequence["RevisionHistoryRequest"],
    ) -> None:
        start_index = 0
        batch_size = 200

        while True:
            end_index = start_index + batch_size
            requests_subset = requests[start_index:end_index]
            if len(requests_subset) == 0:
                break
            start_index = end_index

            with self.session.series.post_fetch_all_vintage_series(
                requests_subset, stream=True
            ) as response:
                _raise_on_error(response)
                ijson_items = ijson.items(response.raw, "item")
                item: "SeriesWithVintagesResponse"
                for item in ijson_items:
                    callback(SeriesWithVintages(item))

    # Search

    def entity_search_multi_filter_long(
        self,
        *filters: "SearchFilter",
        include_discontinued: bool = False,
    ) -> SearchResultLong:
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
            "noMetadata": True,
            "allowLongResult": True,
        }

        response = self.session.search.post_entities(request)

        return SearchResultLong(
            [x["Name"] for x in response["results"]], response.get("isTruncated") is True
        )

    entity_search_multi_filter = entity_search_multi_filter

    # Series

    get_one_series = get_one_series
    get_series = get_series
    get_one_entity = get_one_entity
    get_entities = get_entities
    get_unified_series = get_unified_series
