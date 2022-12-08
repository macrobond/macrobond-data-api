# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_data_api.common import Api

from ._com_api_metadata import (
    metadata_get_attribute_information,
    metadata_get_value_information,
    metadata_list_values,
)

from ._com_api_revision import (
    get_all_vintage_series,
    get_nth_release,
    get_observation_history,
    get_revision_info,
    get_vintage_series,
)

from ._com_api_search import entity_search_multi_filter

from ._com_api_series import (
    get_entities,
    get_one_entity,
    get_series,
    get_one_series,
    get_unified_series,
)

if TYPE_CHECKING:  # pragma: no cover
    from macrobond_data_api.com.com_types import Connection

    from .com_types import Connection, Database

__pdoc__ = {
    "ComApi.__init__": False,
}


class ComApi(Api):
    def __init__(self, connection: "Connection") -> None:
        super().__init__()
        self.__connection = connection

    @property
    def connection(self) -> "Connection":
        return self.__connection

    @property
    def database(self) -> "Database":
        return self.__connection.Database

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

    # Search

    entity_search_multi_filter = entity_search_multi_filter

    # Series

    get_one_series = get_one_series

    get_series = get_series

    get_one_entity = get_one_entity

    get_entities = get_entities

    get_unified_series = get_unified_series
