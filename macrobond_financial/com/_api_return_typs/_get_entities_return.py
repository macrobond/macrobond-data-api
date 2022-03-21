# -*- coding: utf-8 -*-

from typing import Tuple, List, TYPE_CHECKING

from macrobond_financial.common.typs import (
    Entity,
    GetEntitiesError,
)

from macrobond_financial.common.api_return_typs import GetEntitiesReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._series_helps import _create_entity, _create_entity_dicts

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..com_typs import (
        Database,
        Entity as ComEntity,
    )

    from macrobond_financial.common.typs import EntityTypedDict


class _GetEntitiesReturn(GetEntitiesReturn):
    def __init__(
        self, database: "Database", entity_names: Tuple[str, ...], _raise: bool
    ) -> None:
        self.__database = database
        self.__entity_names = entity_names
        self.__raise = _raise

    def fetch_entities(self) -> Tuple["ComEntity", ...]:
        com_entitys = self.__database.FetchEntities(self.__entity_names)
        GetEntitiesError.raise_if(
            self.__raise,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                self.__entity_names,
                com_entitys,
            ),
        )
        return com_entitys

    def list_of_objects(self) -> List[Entity]:
        return list(map(_create_entity, self.fetch_entities(), self.__entity_names))

    def list_of_dicts(self) -> List["EntityTypedDict"]:
        return list(
            map(_create_entity_dicts, self.fetch_entities(), self.__entity_names)
        )

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)
