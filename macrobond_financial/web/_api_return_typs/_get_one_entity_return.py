# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import TYPE_CHECKING

from macrobond_financial.common.types import Entity

from macrobond_financial.common.api_return_typs import GetOneEntityReturn

from ._series_helps import _create_entity

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetOneEntityReturn(GetOneEntityReturn):
    def __init__(self, session: "Session", entity_name: str, _raise: bool) -> None:
        super().__init__(entity_name, _raise)
        self._session = session

    def _object(self) -> Entity:
        response = self._session.series.fetch_entities(self._entity_name)[0]
        return _create_entity(response, self._entity_name)
