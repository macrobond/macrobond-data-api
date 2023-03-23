from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Callable, Tuple

import ijson  # type: ignore


from macrobond_data_api.common.types import SearchResultLong
from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601


from .web_types.subscription_list_state import SubscriptionListState
from .web_types.subscription_list_item import SubscriptionListItem
from .web_types.subscription_list import SubscriptionList
from .web_types.subscription_body import SubscriptionBody


from .session import _raise_on_error

if TYPE_CHECKING:  # pragma: no cover
    from macrobond_data_api.common.types import SearchFilter

    from .web_api import WebApi
    from .web_types.search import SearchRequest, SearchFilter as WebSearchFilter


__pdoc__ = {
    "WebApi.__init__": False,
}


def _get_subscription_list_iterative_pars_body(
    ijson_parse: Any,
) -> Tuple[Optional[datetime], Optional[datetime], Optional[SubscriptionListState]]:
    time_stamp_for_if_modified_since: Optional[datetime] = None
    download_full_list_on_or_after: Optional[datetime] = None
    state: Optional[SubscriptionListState] = None
    for prefix, event, value in ijson_parse:
        if prefix == "timeStampForIfModifiedSince":
            if event != "string":
                raise Exception("bad format: timeStampForIfModifiedSince is not a string")
            time_stamp_for_if_modified_since = _parse_iso8601(value)
        elif prefix == "downloadFullListOnOrAfter":
            if event != "string":
                raise Exception("bad format: downloadFullListOnOrAfter is not a string")
            download_full_list_on_or_after = _parse_iso8601(value)
        elif prefix == "state":
            if event != "number":
                raise Exception("bad format: state is not a number")
            state = SubscriptionListState(value)
        elif event == "start_array":
            if prefix != "entities":
                raise Exception("bad format: event start_array do not have a prefix of entities")
            break
    return time_stamp_for_if_modified_since, download_full_list_on_or_after, state


def _get_subscription_list_iterative_pars_items(
    ijson_parse: Any,
    items_callback: Callable[[SubscriptionBody, List[SubscriptionListItem]], Optional[bool]],
    buffer_size: int,
    body: SubscriptionBody,
) -> bool:
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
            if len(items) == buffer_size:
                if items_callback(body, items) is False:
                    return False
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
            modified = _parse_iso8601(value)

    if len(items) != 0:
        return items_callback(body, items) is not False
    return True


def get_subscription_list(self: "WebApi", if_modified_since: datetime = None) -> SubscriptionList:
    # pylint: disable=line-too-long
    """
    Get the items in the subscription list.
    .. Important:: For large lists you might want to use `macrobond_data_api.web.web_api.WebApi.get_subscription_list_iterative`.

    Typically you want to pass the date of time_stamp_for_if_modified_since from response of the previous call
    to get incremental updates.

    Parameters
    ----------
    if_modified_since : datetime
        The timestamp of the property time_stamp_for_if_modified_since from the response of the previous call.
        If not specified, all items will be returned.

    Returns
    -------
    `macrobond_data_api.web.web_types.subscription_list.SubscriptionList`
    """
    # pylint: enable=line-too-long
    return SubscriptionList(self.session.series.get_subscription_list(if_modified_since))


def get_subscription_list_iterative(
    self: "WebApi",
    body_callback: Callable[[SubscriptionBody], Optional[bool]],
    items_callback: Callable[[SubscriptionBody, List[SubscriptionListItem]], Optional[bool]],
    if_modified_since: datetime = None,
    buffer_size: int = 200,
) -> Optional[SubscriptionBody]:
    # pylint: disable=line-too-long
    """
    Process the subscription list in batches.
    This is more efficient since the complete list does not have to be in memory.

    .. Note:: For for continous polling you might want to use `macrobond_data_api.web.subscription_list_poller.SubscriptionListPoller`.

    Typically you want to pass the date of time_stamp_for_if_modified_since from response of the previous call
    to get incremental updates.

    Parameters
    ----------
    body_callback : `Callable[[macrobond_data_api.web.web_types.subscription_body.SubscriptionBody], Optional[bool]]`
        The callback for the body. This call comes first. Return True to continue processing.

    items_callback : Callable[[macrobond_data_api.web.web_types.subscription_body.SubscriptionBody, List[macrobond_data_api.web.web_types.subscription_list_item.SubscriptionListItem]], Optional[bool]]
        The callback for each batch of items. Return True to continue processing.

    if_modified_since : datetime
        The timestamp of the property time_stamp_for_if_modified_since from the response of the previous call.
        If not specified, all items will be returned.

    buffer_size : int
        The maximum number of items to include in each callback
    Returns
    -------
    `macrobond_data_api.web.web_types.subscription_body.SubscriptionBody`
    """
    # pylint: enable=line-too-long
    params = {}
    body: Optional[SubscriptionBody] = None

    if if_modified_since:
        params["ifModifiedSince"] = if_modified_since.isoformat()

    with self.__session.get("v1/series/getsubscriptionlist", params=params, stream=True) as response:
        _raise_on_error(response)
        ijson_parse = ijson.parse(response.raw)

        (
            time_stamp_for_if_modified_since,
            download_full_list_on_or_after,
            state,
        ) = _get_subscription_list_iterative_pars_body(ijson_parse)

        if state is None:
            raise Exception("bad format: state was not found")
        if time_stamp_for_if_modified_since is None:
            raise Exception("bad format: timeStampForIfModifiedSince was not found")
        if not if_modified_since and download_full_list_on_or_after is None:
            raise Exception("bad format: downloadFullListOnOrAfter was not found")

        body = SubscriptionBody(time_stamp_for_if_modified_since, download_full_list_on_or_after, state)
        if body_callback(body) is False:
            return None

        if _get_subscription_list_iterative_pars_items(ijson_parse, items_callback, buffer_size, body) is False:
            return None

        return body


# Search


def entity_search_multi_filter_long(
    self: "WebApi", *filters: "SearchFilter", include_discontinued: bool = False
) -> SearchResultLong:
    """
    Search for time series and other entitites.
    This call can return more results than `macrobond_data_api.common.api.Api.entity_search_multi_filter`,
    but is also slower and cannot return any metadata.
    You can pass more than one search filter. In this case the filters have to use different
    entity types and searches will be nested so that the result of the previous filter will be
    used as a condition in the subsequent filter linked by the entity type.

    Parameters
    ----------
    *filters : `macrobond_data_api.common.types.search_filter.SearchFilter`
        One or more search filters.
    include_discontinued : bool
        Set this value to True in order to include discontinued entities in the search.

    Returns
    -------
    `macrobond_data_api.common.types.search_result_long.SearchResultLong`
    """

    def convert_filter_to_web_filter(_filter: "SearchFilter") -> "WebSearchFilter":
        return {
            "text": _filter.text,
            "entityTypes": list(_filter.entity_types),
            "mustHaveValues": _filter.must_have_values,
            "mustNotHaveValues": _filter.must_not_have_values,
            "mustHaveAttributes": list(_filter.must_have_attributes),
            "mustNotHaveAttributes": list(_filter.must_not_have_attributes),
        }

    request: "SearchRequest" = {
        "filters": [convert_filter_to_web_filter(x) for x in filters],
        "includeDiscontinued": include_discontinued,
        "noMetadata": True,
        "allowLongResult": True,
    }

    response = self.session.search.post_entities(request)

    return SearchResultLong([x["Name"] for x in response["results"]], response.get("isTruncated") is True)
