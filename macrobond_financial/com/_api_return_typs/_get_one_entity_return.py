# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_financial.common.typs import Entity
from macrobond_financial.common.api_return_typs import GetOneEntityReturn

from ._fill_metadata_from_entity import _fill_metadata_from_entity


if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database


class _GetOneEntityReturn(GetOneEntityReturn):
    def __init__(self, database: "Database", entity_name: str, _raise: bool) -> None:
        super().__init__(entity_name, _raise)
        self._database = database

    def _object(self) -> Entity:
        entity = self._database.FetchOneEntity(self._entity_name)
        if entity.IsError:
            return Entity(self._entity_name, entity.ErrorMessage, None)
        return Entity(self._entity_name, None, _fill_metadata_from_entity(entity))
