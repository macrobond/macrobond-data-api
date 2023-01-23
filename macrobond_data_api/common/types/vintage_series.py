# -*- coding: utf-8 -*-

from datetime import datetime

from typing import List
from typing_extensions import Literal
from dateutil import parser  # type: ignore

from .series import Series, SeriesColumnsLiterals


VintageSeriesColumns = List[Literal[SeriesColumnsLiterals, "VintageTimeStamp", "TimesOfChange"]]


class VintageSeries(Series):
    """Represtents a vintage series"""

    @property
    def revision_time_stamp(self) -> datetime:
        """The vintage of the series."""
        revision_time_stamp = self.metadata["RevisionTimeStamp"]
        if isinstance(revision_time_stamp, list):
            revision_time_stamp = revision_time_stamp[0]

        return (
            parser.parse(revision_time_stamp)
            if isinstance(revision_time_stamp, str)
            else revision_time_stamp
        )
