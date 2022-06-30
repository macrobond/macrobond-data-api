# -*- coding: utf-8 -*-

"""
Definitions of common types used in the API.
"""

from .search_result import SearchResult
from .start_or_end_point import StartOrEndPoint
from .series_entry import SeriesEntry
from .search_filter import SearchFilter
from .metadata_attribute_information import MetadataAttributeInformation
from .series import Series, SeriesColumns

from .entity import Entity, EntityColumns

from .unified_series import (
    UnifiedSeries,
    UnifiedSerie,
    UnifiedSeriesDict,
    UnifiedSeriesColumns,
)

from .vintage_series import VintageSeries

from .metadata_value_information import (
    MetadataValueInformation,
    MetadataValueInformationItem,
    TypedDictMetadataValueInformation,
    MetadataValueInformationColumns,
)

from .get_entitie_error import EntitieErrorInfo, GetEntitiesError

from .metadata_attribute_information import (
    TypedDictMetadataAttributeInformation,
    MetadataAttributeInformationColumns,
)

from .series_observation_history import (
    SeriesObservationHistory,
    SeriesObservationHistoryColumns,
)

from .revision_info import RevisionInfo, RevisionInfoDict

from .get_all_vintage_series_result import GetAllVintageSeriesResult
