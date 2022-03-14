# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING

from datetime import datetime, timezone

from .series import Series

if TYPE_CHECKING:  # pragma: no cover

    from .series import SeriesColumnsLiterals, SeriesTypedDict

    from typing_extensions import Literal

    VintageSeriesColumns = List[
        Literal[SeriesColumnsLiterals, "VintageTimeStamp", "TimesOfChange"]
    ]

    class VintageSeriesTypedDict(SeriesTypedDict, total=False):
        ...


class VintageSeries(Series):
    @property
    def revision_time_stamp(self) -> datetime:
        """The name of the entity."""
        revision_time_stamp = self.metadata["RevisionTimeStamp"]
        if isinstance(revision_time_stamp, list):
            revision_time_stamp = revision_time_stamp[0]

        if isinstance(revision_time_stamp, str):
            return datetime.strptime(revision_time_stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc
            )
        return revision_time_stamp
