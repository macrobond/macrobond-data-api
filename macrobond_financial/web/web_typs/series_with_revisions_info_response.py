# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Optional, List

from .status_response import StatusResponse


class SeriesWithRevisionsInfoResponse(StatusResponse):
    '''Information about a series related to storage of updates'''

    storesRevisions: Optional[bool]
    '''If True, a record of of updates of the series are stored'''

    hasRevisions: Optional[bool]
    '''If True, at least one update has been stored'''

    timeStampOfFirstRevision: Optional[str]
    '''The timestamp of the first recorded update'''

    timeStampOfLastRevision: Optional[str]
    '''The timestamp of the last recorded update'''

    vintageTimeStamps: Optional[List[str]]
    '''A list of timestamp of recorded updates'''
