# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Sequence, List, TYPE_CHECKING

from macrobond_financial.common.typs import Entity, GetEntitiesError

from macrobond_financial.common.api_return_typs import GetEntitiesReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._series_helps import _create_entity, _create_entity_dicts

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from pandas import DataFrame  # type: ignore

    from macrobond_financial.common.typs import EntityTypedDict

    from ..web_typs import EntityResponse


class _GetEntitiesReturn(GetEntitiesReturn):
    def __init__(
        self, session: "Session", entity_names: Sequence[str], _raise: bool
    ) -> None:
        self._session = session
        self._entity_names = entity_names
        self._raise = _raise

    def fetch_entities(self) -> List["EntityResponse"]:
        response = self._session.series.fetch_entities(*self._entity_names)
        GetEntitiesError.raise_if(
            self._raise,
            map(lambda x, y: (x, y.get("errorText")), self._entity_names, response),
        )
        return response

    def list_of_objects(self) -> List[Entity]:
        response = self.fetch_entities()
        return list(map(_create_entity, response, self._entity_names))

    def list_of_dicts(self) -> List["EntityTypedDict"]:
        response = self.fetch_entities()
        return list(map(_create_entity_dicts, response, self._entity_names))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)
