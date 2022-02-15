# -*- coding: utf-8 -*-

from typing import List, Any, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:  # pragma: no cover
    from .enums import MetadataAttributeType


class MetaDirectoryMethods(ABC):

    @abstractmethod
    def list_values(self, name: str) -> List['MetadataValueInformation']:
        '''List all metadata attribute values.'''

    @abstractmethod
    def get_attribute_information(self, name: str) -> 'MetadataAttributeInformation':
        '''Get information about a type of metadata.'''


class MetadataValueInformation():
    '''Information about a metadata value'''

    def __init__(
        self, attribute_name: str, value: Any, description: str, comment: Optional[str]
    ) -> None:
        self.__attribute_name = attribute_name
        self.__value = value
        self.__description = description
        self.__comment = comment

    def __str__(self):
        return self.__attribute_name

    def __repr__(self):
        return str(self)

    @property
    def attribute_name(self) -> str:
        '''The name of the metadata attribute'''
        return self.__attribute_name

    @property
    def value(self) -> Any:
        '''The value'''
        return self.__value

    @property
    def description(self) -> str:
        '''The description of the metadata value'''
        return self.__description

    @property
    def comment(self) -> Optional[str]:
        '''The comment of the metadata value'''
        return self.__comment

    def __eq__(self, other):
        if not isinstance(other, MetadataValueInformation):
            return NotImplemented

        return \
            self is other or \
            (
                self.__attribute_name == other.attribute_name and
                self.__value == other.value and
                self.__description == other.description and
                self.__comment == other.comment
            )

    def __hash__(self):
        return hash((
            self.__attribute_name,
            self.__value,
            self.__description,
            self.__comment
        ))


class MetadataAttributeInformation():
    '''Information about a metadata attribute'''

    def __init__(
        self, name: str, description: str, comment: Optional[str],
        value_type: 'MetadataAttributeType',
        uses_value_list: bool, can_list_values: bool, can_have_multiple_values: bool,
        is_database_entity: bool
    ) -> None:
        self.__name = name
        self.__description = description
        self.__comment = comment
        self.__value_type = value_type
        self.__uses_value_list = uses_value_list
        self.__can_list_values = can_list_values
        self.__can_have_multiple_values = can_have_multiple_values
        self.__is_database_entity = is_database_entity

    def __str__(self):
        return self.__name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, MetadataAttributeInformation):
            return NotImplemented

        return \
            self is other or \
            (
                self.__name == other.name and
                self.__description == other.description and
                self.__comment == other.comment and
                self.__uses_value_list == other.uses_value_list and
                self.__can_list_values == other.can_list_values and
                self.__can_have_multiple_values == other.can_have_multiple_values and
                self.__is_database_entity == other.is_database_entity
            )

    def __hash__(self):
        return hash((
            self.__name,
            self.__description,
            self.__comment,
            self.__uses_value_list,
            self.__can_list_values,
            self.__can_have_multiple_values,
            self.__is_database_entity
        ))

    @property
    def name(self) -> str:
        '''The name of the metadata attribute'''
        return self.__name

    @property
    def description(self) -> str:
        '''The description of the metadata attribute'''
        return self.__description

    @property
    def comment(self) -> Optional[str]:
        '''The comment of the metadata attribute'''
        return self.__comment

    @property
    def value_type(self) -> 'MetadataAttributeType':
        '''The value type of the metadata attribute'''
        return self.__value_type

    @property
    def uses_value_list(self) -> bool:
        '''If True, the metadata attribute uses a list of values'''
        return self.__uses_value_list

    @property
    def can_list_values(self) -> bool:
        '''
        If True then the values of this type of
        metadata can be listen using the ListAllValues function
        '''
        return self.__can_list_values

    @property
    def can_have_multiple_values(self) -> bool:
        '''If True then this type of metadata can have multiple values in a metadata collection'''
        return self.__can_have_multiple_values

    @property
    def is_database_entity(self) -> bool:
        '''
        If True then this type of metadata is an entity that can be retrieved from the database
        '''
        return self.__is_database_entity
