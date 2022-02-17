# -*- coding: utf-8 -*-
'''module doc string'''

from typing import List, Any, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:  # pragma: no cover
    from .enums import MetadataAttributeType


class MetaDirectoryMethods(ABC):
    '''
    This class fetches methods to look up metadata
    '''

    @abstractmethod
    def list_values(self, name: str) -> List['MetadataValueInformation']:
        '''
        List all metadata attribute values.

        Parameters
        ----------
        name : str
            record that failed processing

        Returns
        -------
        List[MetadataValueInformation]
            "success", result, original record

        Examples
        -------
        ```python
        with ComClient() as api: # or WebClient
            value_information_list = api.meta_directory.list_values('RateType')
            for info in value_information_list:
                print(info.value + ' ' + info.description)
        ```
        '''

    @abstractmethod
    def get_attribute_information(self, name: str) -> 'MetadataAttributeInformation':
        '''Get information about a type of metadata.'''


class MetadataValueInformation():
    '''Information about a metadata value'''

    attribute_name: str
    '''The name of the metadata attribute'''

    value: Any
    '''The value'''

    description: str
    '''The description of the metadata value'''

    comment: Optional[str]
    '''The comment of the metadata value'''

    def __init__(
        self, attribute_name: str, value: Any, description: str, comment: Optional[str]
    ) -> None:
        self.attribute_name = attribute_name
        self.value = value
        self.description = description
        self.comment = comment

    def __str__(self):
        return self.attribute_name

    def __repr__(self):
        return self.attribute_name

    def __eq__(self, other):
        print('am here !')
        if not isinstance(other, MetadataValueInformation):
            return NotImplemented

        return \
            self is other or \
            (
                self.attribute_name == other.attribute_name and
                self.value == other.value and
                self.description == other.description and
                self.comment == other.comment
            )

    def __hash__(self):
        return hash((
            self.attribute_name,
            self.value,
            self.description,
            self.comment
        ))


class MetadataAttributeInformation():
    '''Information about a metadata attribute'''

    name: str
    '''The name of the metadata attribute'''

    description: str
    '''The description of the metadata attribute'''

    comment: Optional[str]
    '''The comment of the metadata attribute'''

    value_type: 'MetadataAttributeType'
    '''The value type of the metadata attribute'''

    uses_value_list: bool
    '''If True, the metadata attribute uses a list of values'''

    can_list_values: bool
    '''
    If True then the values of this type of
    metadata can be listen using the ListAllValues function
    '''

    can_have_multiple_values: bool
    '''If True then this type of metadata can have multiple values in a metadata collection'''

    is_database_entity: bool
    '''
    If True then this type of metadata is an entity that can be retrieved from the database
    '''

    def __init__(
        self, name: str, description: str, comment: Optional[str],
        value_type: 'MetadataAttributeType',
        uses_value_list: bool, can_list_values: bool, can_have_multiple_values: bool,
        is_database_entity: bool
    ) -> None:
        self.name = name
        self.description = description
        self.comment = comment
        self.value_type = value_type
        self.uses_value_list = uses_value_list
        self.can_list_values = can_list_values
        self.can_have_multiple_values = can_have_multiple_values
        self.is_database_entity = is_database_entity

    def __str__(self):
        return self.name + ' ' + self.description

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, MetadataAttributeInformation):
            return NotImplemented

        return \
            self is other or \
            (
                self.name == other.name and
                self.description == other.description and
                self.comment == other.comment and
                self.uses_value_list == other.uses_value_list and
                self.can_list_values == other.can_list_values and
                self.can_have_multiple_values == other.can_have_multiple_values and
                self.is_database_entity == other.is_database_entity
            )

    def __hash__(self):
        return hash((
            self.name,
            self.description,
            self.comment,
            self.uses_value_list,
            self.can_list_values,
            self.can_have_multiple_values,
            self.is_database_entity
        ))
