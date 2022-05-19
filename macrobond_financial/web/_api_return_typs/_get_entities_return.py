# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Tuple, List, TYPE_CHECKING

from macrobond_financial.common.typs import Entity

from macrobond_financial.common.api_return_typs import GetEntitiesReturn

from ._series_helps import _create_entity

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetEntitiesReturn(GetEntitiesReturn):
    def __init__(
        self, session: "Session", entity_names: Tuple[str, ...], _raise: bool
    ) -> None:
        super().__init__(entity_names, _raise)
        self._session = session

    def _list_of_objects(self) -> List[Entity]:
        response = self._session.series.fetch_entities(*self._entity_names)
        return list(map(_create_entity, response, self._entity_names))
