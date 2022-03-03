# -*- coding: utf-8 -*-

from typing import List, cast, TYPE_CHECKING

from macrobond_financial.common._get_pandas import _get_pandas

import macrobond_financial.common.meta_directory_methods as MetaDirectoryMethods

from macrobond_financial.common.metadata_value_information import (
    MetadataValueInformation,
)
from macrobond_financial.common.metadata_attribute_information import (
    MetadataAttributeInformation,
)

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from .com_typs import (
        Connection,
        Database,
        MetadataValueInformation as ComMetadataValueInformation,
    )

    from macrobond_financial.common.enums import MetadataAttributeType

    from macrobond_financial.common import (
        TypedDictMetadataValueInformation,
        TypedDictMetadataAttributeInformation,
    )


class _ListValuesReturn(MetaDirectoryMethods.ListValuesReturn):
    def __init__(self, database: "Database", name: str) -> None:
        super().__init__()
        self.__database = database
        self.__name = name

    def list_of_objects(self) -> List[MetadataValueInformation]:
        info = self.__database.GetMetadataInformation(self.__name)
        values = info.ListAllValues()

        def to_object(
            info: "ComMetadataValueInformation",
        ) -> "MetadataValueInformation":
            return MetadataValueInformation(
                self.__name, info.Value, info.Description, info.Comment
            )

        return list(map(to_object, values))

    def list_of_dicts(self) -> List["TypedDictMetadataValueInformation"]:
        info = self.__database.GetMetadataInformation(self.__name)
        values = info.ListAllValues()

        def to_dict(
            info: "ComMetadataValueInformation",
        ) -> "TypedDictMetadataValueInformation":
            return {
                "attribute_name": self.__name,
                "value": info.Value,
                "description": info.Description,
                "comment": info.Comment,
            }

        return list(map(to_dict, values))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetAttributeInformationReturn(
    MetaDirectoryMethods.GetAttributeInformationReturn
):
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


class _ComMetaDirectoryMethods(MetaDirectoryMethods.MetaDirectoryMethods):
    def __init__(self, connection: "Connection") -> None:
        super().__init__()
        self.__database = connection.Database

    def list_values(self, name: str) -> MetaDirectoryMethods.ListValuesReturn:
        return _ListValuesReturn(self.__database, name)

    def get_attribute_information(
        self, name: str
    ) -> MetaDirectoryMethods.GetAttributeInformationReturn:
        return _GetAttributeInformationReturn(self.__database, name)
