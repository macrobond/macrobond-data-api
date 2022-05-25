# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Optional, List

from .series_response import SeriesResponse


class SeriesWithTimesOfChangeResponse(SeriesResponse):
    """A time series with times of change"""

    timesOfChange: Optional[List[Optional[str]]]
    """The time each value was last modified"""
