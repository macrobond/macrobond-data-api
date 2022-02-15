# -*- coding: utf-8 -*-

from abc import ABC
from .meta_directory_methods import MetaDirectoryMethods
from .search_methods import SearchMethods
from .series_methods import SeriesMethods

__pdoc__ = {
    'Api.__init__': False,
}


class Api(ABC):

    @property
    def meta_directory(self) -> MetaDirectoryMethods:
        return self.__meta_directory

    @property
    def search(self) -> SearchMethods:
        return self.__search

    @property
    def series(self) -> SeriesMethods:
        return self.__series

    def __init__(
        self, meta_directory: MetaDirectoryMethods, search: SearchMethods, series: SeriesMethods
    ) -> None:
        self.__meta_directory = meta_directory
        self.__search = search
        self.__series = series
