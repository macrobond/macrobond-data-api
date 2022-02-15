# -*- coding: utf-8 -*-

from .enums import *
from .meta_directory_methods import *
from .search_methods import SearchMethods, SearchFilter, SearchResult
from .series_methods import Series, Entity, UnifiedSeries, Metadata, StartOrEndPoint, \
    SeriesEntrie, SeriesMethods
from .client import Client
from .api import Api

__all__ = [
    'Client', 'Api', 'Series', 'Entity', 'UnifiedSeries', 'Metadata', 'StartOrEndPoint',
    'SeriesEntrie', 'SeriesMethods', 'SearchMethods', 'SearchFilter', 'SearchResult'
]

__pdoc__ = {
    'Api.__init__': False,
    'StartOrEndPoint.__init__': False,
    # 'macrobond_financial.common.api': False,
    # 'macrobond_financial.common.client': False,
    # 'macrobond_financial.common.series_methods': False,
    # 'macrobond_financial.common.meta_directory_methods': False,
}
