from typing import TYPE_CHECKING, Optional

from macrobond_data_api.common import Api

from ._com_api_metadata import (
    metadata_get_attribute_information,
    metadata_get_value_information,
    metadata_list_values,
)

from ._com_api_revision import (
    get_all_vintage_series,
    get_one_nth_release,
    get_nth_release,
    get_observation_history,
    get_revision_info,
    get_one_vintage_series,
    get_vintage_series,
    get_many_series_with_revisions,
)

from ._com_api_search import entity_search_multi_filter

from ._com_api_series import (
    get_entities,
    get_one_entity,
    get_series,
    get_one_series,
    get_many_series,
    get_unified_series,
)

if TYPE_CHECKING:  # pragma: no cover
    from macrobond_data_api.com.com_types import Connection

    from .com_types import Connection, Database

__pdoc__ = {
    "ComApi.__init__": False,
}


class ComApi(Api):
    _connection: Optional["Connection"]

    def __init__(self, connection: "Connection") -> None:
        super().__init__()
        self._connection = connection

    @property
    def connection(self) -> "Connection":
        if self._connection is None:
            raise ValueError("ComApi is not open")
        return self._connection

    @property
    def database(self) -> "Database":
        return self.connection.Database

    # metadata

    metadata_list_values = metadata_list_values
    metadata_get_attribute_information = metadata_get_attribute_information
    metadata_get_value_information = metadata_get_value_information

    # revision

    get_revision_info = get_revision_info
    get_one_vintage_series = get_one_vintage_series
    get_vintage_series = get_vintage_series
    get_one_nth_release = get_one_nth_release
    get_nth_release = get_nth_release
    get_all_vintage_series = get_all_vintage_series
    get_observation_history = get_observation_history
    get_many_series_with_revisions = get_many_series_with_revisions

    # Search

    entity_search_multi_filter = entity_search_multi_filter

    # Series

    get_one_series = get_one_series
    get_series = get_series
    get_one_entity = get_one_entity
    get_entities = get_entities
    get_many_series = get_many_series
    get_unified_series = get_unified_series
