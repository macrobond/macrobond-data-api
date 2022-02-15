# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Optional, TypedDict, List, Dict


class SearchResponse(TypedDict):
    '''Entity search response'''

    isTruncated: Optional[bool]
    '''If True, the search response is truncated'''

    results: List[Dict[str, object]]
    '''The matched entites'''
