from macrobond_data_api.common import Api

from ._web_only_api import entity_search_multi_filter_long, get_subscription_list, get_subscription_list_iterative

from ._web_api_metadata import metadata_list_values, metadata_get_attribute_information, metadata_get_value_information

from ._web_api_revision import (
    get_all_vintage_series,
    get_nth_release,
    get_revision_info,
    get_vintage_series,
    get_observation_history,
    get_many_series_with_revisions,
)

from ._web_api_series import (
    get_one_series,
    get_series,
    get_one_entity,
    get_entities,
    get_many_series,
    get_unified_series,
)

from ._web_api_search import entity_search_multi_filter

from .session import Session


__pdoc__ = {
    "WebApi.__init__": False,
}


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
    get_many_series_with_revisions = get_many_series_with_revisions

    # web only

    get_subscription_list = get_subscription_list
    get_subscription_list_iterative = get_subscription_list_iterative
    entity_search_multi_filter_long = entity_search_multi_filter_long

    # Search

    entity_search_multi_filter = entity_search_multi_filter

    # Series

    get_one_series = get_one_series
    get_series = get_series
    get_one_entity = get_one_entity
    get_entities = get_entities
    get_many_series = get_many_series
    get_unified_series = get_unified_series
