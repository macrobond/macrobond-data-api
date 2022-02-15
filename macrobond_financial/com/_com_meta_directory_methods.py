# -*- coding: utf-8 -*-

from typing import List, cast, TYPE_CHECKING

from macrobond_financial.common import MetaDirectoryMethods, MetadataValueInformation, \
    MetadataAttributeInformation

if TYPE_CHECKING:  # pragma: no cover
    from .com_typs import Connection
    from macrobond_financial.common.enums import MetadataAttributeType


class _ComMetaDirectoryMethods(MetaDirectoryMethods):

    def __init__(self, connection: 'Connection') -> None:
        super().__init__()
        self.__database = connection.Database

    def list_values(self, name: str) -> List[MetadataValueInformation]:
        info = self.__database.GetMetadataInformation(name)

        values = info.ListAllValues()

        return list(map(
            lambda x: MetadataValueInformation(name, x.Value, x.Description, x.Comment), values))

    def get_attribute_information(self, name: str) -> MetadataAttributeInformation:
        info = self.__database.GetMetadataInformation(name)
        return MetadataAttributeInformation(
            info.Name,
            info.Description,
            info.Comment,
            cast('MetadataAttributeType', info.ValueType),
            info.UsesValueList,
            info.CanListValues,
            info.CanHaveMultipleValues,
            info.IsDatabaseEntity,
        )
