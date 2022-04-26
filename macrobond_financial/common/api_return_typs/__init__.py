# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from .get_attribute_information_return import GetAttributeInformationReturn
from .get_entities_return import GetEntitiesReturn
from .get_nth_release_return import GetNthReleaseReturn
from .get_observation_history_return import GetObservationHistoryReturn
from .get_one_entity_return import GetOneEntityReturn
from .get_one_series_return import GetOneSeriesReturn
from .get_revision_info_return import GetRevisionInfoReturn, RevisionInfo

from .get_series_return import GetSeriesReturn
from .get_unified_series_return import GetUnifiedSeriesReturn
from .get_vintage_series_return import GetVintageSeriesReturn
from .list_values_return import ListValuesReturn


if TYPE_CHECKING:  # pragma: no cover

    from .get_revision_info_return import RevisionInfoDict
