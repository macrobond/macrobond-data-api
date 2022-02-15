# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Optional, TypedDict, Any


class MetadataValueInformationResponse(TypedDict, total=False):
    '''Information about a metadata value'''

    attributeName: str
    '''The name of the metadata attribute'''

    value: Any
    '''The value'''

    description: str
    '''The description of the metadata value'''

    comment: Optional[str]
    '''The comment of the metadata value'''
