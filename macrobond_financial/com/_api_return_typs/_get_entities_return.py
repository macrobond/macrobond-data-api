# -*- coding: utf-8 -*-

from typing import Tuple, List, TYPE_CHECKING

from macrobond_financial.common.typs import Entity

from macrobond_financial.common.api_return_typs import GetEntitiesReturn

from ._series_helps import _create_entity

if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database


class _GetEntitiesReturn(GetEntitiesReturn):
    def __init__(
        self, database: "Database", entity_names: Tuple[str, ...], _raise: bool
    ) -> None:
        super().__init__(entity_names, _raise)
        self.__database = database

    def _list_of_objects(self) -> List[Entity]:
        com_entitys = self.__database.FetchEntities(self._entity_names)
        return list(map(_create_entity, com_entitys, self._entity_names))
