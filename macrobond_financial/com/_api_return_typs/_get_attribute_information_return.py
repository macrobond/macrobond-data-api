# -*- coding: utf-8 -*-

from typing import cast, TYPE_CHECKING

from macrobond_financial.common._get_pandas import _get_pandas

from macrobond_financial.common.api_return_typs import GetAttributeInformationReturn

from macrobond_financial.common.typs import (
    MetadataAttributeInformation,
)

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..com_typs import (
        Database,
    )

    from macrobond_financial.common.enums import MetadataAttributeType

    from macrobond_financial.common.typs import TypedDictMetadataAttributeInformation


class _GetAttributeInformationReturn(GetAttributeInformationReturn):
    def __init__(self, database: "Database", name: str) -> None:
        super().__init__()
        self.__database = database
        self.__name = name

    def object(self) -> MetadataAttributeInformation:
        info = self.__database.GetMetadataInformation(self.__name)
        return MetadataAttributeInformation(
            info.Name,
            info.Description,
            info.Comment,
            cast("MetadataAttributeType", info.ValueType),
            info.UsesValueList,
            info.CanListValues,
            info.CanHaveMultipleValues,
            info.IsDatabaseEntity,
        )

    def dict(self) -> "TypedDictMetadataAttributeInformation":
        info = self.__database.GetMetadataInformation(self.__name)
        return {
            "name": info.Name,
            "description": info.Description,
            "comment": info.Comment,
            "value_type": cast("MetadataAttributeType", info.ValueType),
            "uses_value_list": info.UsesValueList,
            "can_list_values": info.CanListValues,
            "can_have_multiple_values": info.CanHaveMultipleValues,
            "is_database_entity": info.IsDatabaseEntity,
        }

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)
