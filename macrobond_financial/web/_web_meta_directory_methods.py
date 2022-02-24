# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import List, cast, TYPE_CHECKING

from macrobond_financial.common._get_pandas import _get_pandas

import macrobond_financial.common.meta_directory_methods as MetaDirectoryMethods

from macrobond_financial.common.metadata_value_information import MetadataValueInformation
from macrobond_financial.common.metadata_attribute_information import MetadataAttributeInformation

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from .session import Session

    from macrobond_financial.common.enums import MetadataAttributeType

    from macrobond_financial.common import \
        TypedDictMetadataValueInformation, TypedDictMetadataAttributeInformation

    from .web_typs.metadata_value_information_response import MetadataValueInformationItem


class _ListValuesReturn(MetaDirectoryMethods.ListValuesReturn):

    def __init__(self, session: 'Session', name: str) -> None:
        super().__init__()
        self.__session = session
        self.__name = name

    def list_of_objects(self) -> List[MetadataValueInformation]:
        values = self.__session.metadata.list_attribute_values(self.__name)
        return list(map(
            lambda x: MetadataValueInformation(
                self.__name, x['value'], x['description'], x.get('comment')
            ), values)
        )

    def list_of_dicts(self) -> List['TypedDictMetadataValueInformation']:
        values = self.__session.metadata.list_attribute_values(self.__name)

        def to_dict(
            info: 'MetadataValueInformationItem'
        ) -> 'TypedDictMetadataValueInformation':
            return {
                'attribute_name': self.__name,
                'value': info['value'],
                'description': info['description'],
                'comment': info.get('comment')
            }
        return list(map(to_dict, values))

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        pandas = _get_pandas()
        args = args[1:]
        kwargs['data'] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetAttributeInformationReturn(MetaDirectoryMethods.GetAttributeInformationReturn):

    def __init__(self, session: 'Session', name: str) -> None:
        super().__init__()
        self.__session = session
        self.__name = name

    def object(self) -> MetadataAttributeInformation:
        info = self.__session.metadata.get_attribute_information(self.__name)[0]
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

    def dict(self) -> 'TypedDictMetadataAttributeInformation':
        info = self.__session.metadata.get_attribute_information(self.__name)[0]
        return {
            'name': info['name'],
            'description': info['description'],
            'comment': info.get('comment'),
            'value_type': cast('MetadataAttributeType', info['valueType']),
            'uses_value_list': info['usesValueList'],
            'can_list_values': info['canListValues'],
            'can_have_multiple_values': info['canHaveMultipleValues'],
            'is_database_entity': info['isDatabaseEntity'],
        }

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        pandas = _get_pandas()
        args = args[1:]
        kwargs['data'] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)


class _WebMetaDirectoryMethods(MetaDirectoryMethods.MetaDirectoryMethods):

    def __init__(self, session: 'Session') -> None:
        super().__init__()
        self.__session = session

    def list_values(self, name: str) -> MetaDirectoryMethods.ListValuesReturn:
        return _ListValuesReturn(self.__session, name)

    def get_attribute_information(
        self, name: str
    ) -> MetaDirectoryMethods.GetAttributeInformationReturn:
        return _GetAttributeInformationReturn(self.__session, name)
