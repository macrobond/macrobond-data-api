# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_financial.common import Api

from ._web_meta_directory_methods import _WebMetaDirectoryMethods
from ._web_search_methods import _WebSearchMethods
from ._web_series_methods import _WebSeriesMethods

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session

__pdoc__ = {
    'WebApi.__init__': False,
}


class WebApi(Api):

    @property
    def session(self) -> 'Session':
        return self.__session

    def __init__(self, session: 'Session') -> None:
        super().__init__(
            _WebMetaDirectoryMethods(session),
            _WebSearchMethods(session),
            _WebSeriesMethods(session)
        )
        self.__session = session
