# -*- coding: utf-8 -*-

from typing import cast, TYPE_CHECKING

from macrobond_financial.common.api_return_typs import GetAttributeInformationReturn

from macrobond_financial.common.types import MetadataAttributeInformation

if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database

    from macrobond_financial.common.enums import MetadataAttributeType


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
