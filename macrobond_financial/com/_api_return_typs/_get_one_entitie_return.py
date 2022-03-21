# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_financial.common.typs import (
    Entity,
    GetEntitiesError,
)
from macrobond_financial.common.api_return_typs import GetOneEntitieReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._fill_metadata_from_entity import _fill_metadata_from_entity

from ._series_helps import _create_entity, _create_entity_dicts

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..com_typs import (
        Database,
        Entity as ComEntity,
    )

    from macrobond_financial.common.typs import EntityTypedDict


class _GetOneEntitieReturn(GetOneEntitieReturn):
    def __init__(self, database: "Database", entity_name: str, _raise: bool) -> None:
        self.__database = database
        self.__entity_name = entity_name
        self.__raise = _raise

    def fetch_one_entity(self) -> "ComEntity":
        com_entity = self.__database.FetchOneEntity(self.__entity_name)
        if self.__raise and com_entity.IsError:
            raise GetEntitiesError(self.__entity_name, com_entity.ErrorMessage)
        return com_entity

    def object(self) -> Entity:
        return _create_entity(self.fetch_one_entity(), self.__entity_name)

    def dict(self) -> "EntityTypedDict":
        return _create_entity_dicts(self.fetch_one_entity(), self.__entity_name)

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def metadata_as_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()

        entity = self.fetch_one_entity()
        return pandas.DataFrame.from_dict(
            _fill_metadata_from_entity(entity), orient="index", columns=["Attributes"]
        )
