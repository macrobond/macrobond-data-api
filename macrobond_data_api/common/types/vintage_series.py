from dataclasses import dataclass
from datetime import datetime

from typing import List, Optional, Sequence, TYPE_CHECKING
from typing_extensions import Literal
from dateutil import parser

from .series import Series, SeriesColumnsLiterals

if TYPE_CHECKING:  # pragma: no cover
    from .metadata import Metadata


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
        metadata: Optional["Metadata"],
        values: Optional[Sequence[Optional[float]]],
        dates: Optional[Sequence[datetime]],
        _revision_time_stamp: Optional[datetime],
    ) -> None:
        super().__init__(name, error_message, metadata, values, dates)
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

        return parser.parse(revision_time_stamp) if isinstance(revision_time_stamp, str) else revision_time_stamp
