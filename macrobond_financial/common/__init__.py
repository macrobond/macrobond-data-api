# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING


from .enums import *
from .meta_directory_methods import *
from .search_methods import SearchMethods, SearchFilter, SearchResult
from .series_methods import SeriesEntrie, SeriesMethods

from .entity import Entity
from .series import Series
from .vintage_series import VintageSeries
from .unified_series import UnifiedSeries, UnifiedSerie
from .start_or_end_point import StartOrEndPoint

from .client import Client
from .api import Api
from .credentials import Credentials

from .get_entitie_error import EntitieErrorInfo, GetEntitiesError

from .enums.series_frequency import SeriesFrequency

if TYPE_CHECKING:
    from .entity import EntityTypedDict
    from .series import SeriesTypedDict
    from .vintage_series import VintageSeriesTypedDict


__all__ = [
    "Client",
    "Api",
    "Series",
    "VintageSeries",
    "Entity",
    "UnifiedSeries",
    "UnifiedSerie",
    "StartOrEndPoint",
    "SeriesEntrie",
    "SeriesMethods",
    "SearchMethods",
    "SearchFilter",
    "SearchResult",
    "Credentials",
    "SeriesFrequency",
    "EntitieErrorInfo",
    "GetEntitiesError",
    "EntityTypedDict",
    "SeriesTypedDict",
    "VintageSeriesTypedDict",
]

__pdoc__ = {"StartOrEndPoint.__init__": False}
