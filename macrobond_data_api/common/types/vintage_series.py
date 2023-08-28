from dataclasses import dataclass
from datetime import datetime

from typing import List, Optional, TYPE_CHECKING, Literal

from macrobond_data_api.common.enums import StatusCode
from .series import Series, SeriesColumnsLiterals

from ._parse_iso8601 import _parse_iso8601

if TYPE_CHECKING:  # pragma: no cover
    from .metadata import Metadata
    from .values_metadata import ValuesMetadata


VintageSeriesColumns = List[Literal[SeriesColumnsLiterals, "VintageTimeStamp", "TimesOfChange"]]


__pdoc__ = {
    "VintageSeries.__init__": False,
}


@dataclass(init=False)
class VintageSeries(Series):
    """Represtents a vintage series"""

    __slots__ = ("_revision_time_stamp",)

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        status_code: StatusCode,
        metadata: Optional["Metadata"],
        values_metadata: Optional["ValuesMetadata"],
        values: Optional[List[Optional[float]]],
        dates: Optional[List[datetime]],
        _revision_time_stamp: Optional[datetime],
    ) -> None:
        super().__init__(name, error_message, status_code, metadata, values_metadata, values, dates)
        self._revision_time_stamp = _revision_time_stamp

    @property
    def revision_time_stamp(self) -> Optional[datetime]:
        """The vintage of the series."""
        if self._revision_time_stamp:
            return self._revision_time_stamp

        if "RevisionTimeStamp" not in self.metadata:
            return None

        revision_time_stamp = self.metadata["RevisionTimeStamp"]
        if isinstance(revision_time_stamp, list):
            revision_time_stamp = revision_time_stamp[0]

        return _parse_iso8601(revision_time_stamp) if isinstance(revision_time_stamp, str) else revision_time_stamp
