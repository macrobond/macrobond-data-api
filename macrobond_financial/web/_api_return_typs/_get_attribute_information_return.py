# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import cast, TYPE_CHECKING

from macrobond_financial.common._get_pandas import _get_pandas

from macrobond_financial.common.api_return_typs import GetAttributeInformationReturn

from macrobond_financial.common.typs import MetadataAttributeInformation

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..session import Session

    from macrobond_financial.common.enums import MetadataAttributeType
    from macrobond_financial.common.typs import (
        TypedDictMetadataAttributeInformation,
    )


class _GetAttributeInformationReturn(GetAttributeInformationReturn):
    def __init__(self, session: "Session", name: str) -> None:
        super().__init__()
        self.__session = session
        self.__name = name

    def object(self) -> MetadataAttributeInformation:
        info = self.__session.metadata.get_attribute_information(self.__name)[0]
        return MetadataAttributeInformation(
            info["name"],
            info["description"],
            info.get("comment"),
            info["valueType"],
            info["usesValueList"],
            info["canListValues"],
            info["canHaveMultipleValues"],
            info["isDatabaseEntity"],
        )

    def dict(self) -> "TypedDictMetadataAttributeInformation":
        info = self.__session.metadata.get_attribute_information(self.__name)[0]
        return {
            "name": info["name"],
            "description": info["description"],
            "comment": info.get("comment"),
            "value_type": cast("MetadataAttributeType", info["valueType"]),
            "uses_value_list": info["usesValueList"],
            "can_list_values": info["canListValues"],
            "can_have_multiple_values": info["canHaveMultipleValues"],
            "is_database_entity": info["isDatabaseEntity"],
        }

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)
