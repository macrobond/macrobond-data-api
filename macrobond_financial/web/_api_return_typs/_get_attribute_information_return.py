# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import TYPE_CHECKING

from macrobond_financial.common.api_return_typs import GetAttributeInformationReturn

from macrobond_financial.common.types import MetadataAttributeInformation

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


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
