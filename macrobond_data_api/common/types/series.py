from dataclasses import dataclass
from datetime import datetime

from typing import Any, Dict, Optional, List, Sequence, TYPE_CHECKING, cast
from typing_extensions import Literal

from .entity import Entity, EntityColumnsLiterals


SeriesColumnsLiterals = Literal[EntityColumnsLiterals, "Values", "Dates"]

SeriesColumns = List[SeriesColumnsLiterals]

if TYPE_CHECKING:  # pragma: no cover
    from pandas import Series as PdSeries  # type: ignore
    from .metadata import Metadata

__pdoc__ = {
    "Series.__init__": False,
}


@dataclass(init=False)
class Series(Entity):
    """Represents a Macrobond time series."""

    __slots__ = ("values", "dates")

    values: Sequence[Optional[float]]
    dates: Sequence[datetime]

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        metadata: Optional["Metadata"],
        values: Optional[Sequence[Optional[float]]],
        dates: Optional[Sequence[datetime]],
    ) -> None:
        super().__init__(name, error_message, metadata)

        self.values = ...  # type: ignore
        """
        The values of the series.
        The number of values is the same as the number of `Series.dates`. 
        """
        self.dates = ...  # type: ignore
        """
        The dates of the periods corresponding to the values
        The number of dates is the same as the number of `Series.values`. 
        """

        if values is None:
            self.values = []
            self.dates = []
        else:
            self.values = values
            self.dates = cast(Sequence[datetime], dates)

    def to_dict(self) -> Dict[str, Any]:
        if self.is_error:
            return {
                "Name": self.name,
                "ErrorMessage": self.error_message,
            }
        ret = {
            "Name": self.name,
            "Values": self.values,
            "Dates": self.dates,
        }
        self._add_metadata(ret)
        return ret

    def values_to_pd_series(self, name: str = None) -> "PdSeries":
        import pandas  # pylint: disable=import-outside-toplevel

        name = name if name else self.name
        return pandas.Series(self.values, self.dates, name=name)

    def _repr_html_(self) -> str:
        return self.metadata_to_pd_series().to_frame()._repr_html_()
