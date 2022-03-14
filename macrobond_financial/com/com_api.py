# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_financial.common import Api

from ._com_meta_directory_methods import _ComMetaDirectoryMethods
from ._com_search_methods import _ComSearchMethods
from ._com_series_methods import _ComSeriesMethods
from ._com_revision_methods import _ComRevisionMethods

if TYPE_CHECKING:  # pragma: no cover
    from macrobond_financial.com.com_typs.connection import Connection

__pdoc__ = {
    "ComApi.__init__": False,
}


class ComApi(Api):
    def __init__(self, connection: "Connection") -> None:
        super().__init__(
            _ComMetaDirectoryMethods(connection),
            _ComSearchMethods(connection),
            _ComSeriesMethods(self),
            _ComRevisionMethods(self),
        )
        self.__connection = connection

    @property
    def connection(self) -> "Connection":
        return self.__connection
