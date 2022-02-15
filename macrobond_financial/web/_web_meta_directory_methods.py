# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import List, TYPE_CHECKING

from macrobond_financial.common import MetaDirectoryMethods, MetadataValueInformation, \
    MetadataAttributeInformation

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session


class _WebMetaDirectoryMethods(MetaDirectoryMethods):

    def __init__(self, session: 'Session') -> None:
        super().__init__()
        self.__session = session

    def list_values(self, name: str) -> List[MetadataValueInformation]:
        values = self.__session.metadata.list_attribute_values(name)
        return list(map(
            lambda x: MetadataValueInformation(
                name, x['value'], x['description'], x.get('comment')
            ), values)
        )

    def get_attribute_information(self, name: str) -> MetadataAttributeInformation:
        info = self.__session.metadata.get_attribute_information(name)[0]
        return MetadataAttributeInformation(
            info['name'],
            info['description'],
            info.get('comment'),
            info['valueType'],
            info['usesValueList'],
            info['canListValues'],
            info['canHaveMultipleValues'],
            info['isDatabaseEntity']
        )
