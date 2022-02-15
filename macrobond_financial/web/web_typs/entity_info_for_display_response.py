# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import List, Optional, TypedDict


from .metadata_attribute_information_response import \
    MetadataAttributeType, MetadataAttributeTypeRestriction


class EntityInfoForDisplayItem(TypedDict):
    # pylint: disable = missing-class-docstring

    description: str
    '''Description of the item'''

    comment: Optional[str]
    '''The comment of the metadata value'''

    valueType: MetadataAttributeType
    '''The value type of the metadata attribute'''

    valueRestriction: Optional[MetadataAttributeTypeRestriction]
    '''Restriction on the value type'''

    value: object
    '''The item value'''


class EntityNameWithTimeStamp(TypedDict):
    # pylint: disable = missing-class-docstring

    description: str
    '''Heading of the group'''

    title: Optional[str]
    '''Title of the group'''

    items: List[EntityInfoForDisplayItem]
    '''List of information items'''


class EntityInfoForDisplayResponse(TypedDict):
    '''Entity search response with metadata displayed for presentation purposes'''

    groups: List['EntityNameWithTimeStamp']
    '''A list of information groups'''
