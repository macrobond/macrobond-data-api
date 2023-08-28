from dataclasses import dataclass
from datetime import datetime

from typing import Any, Dict, Optional, List, Sequence, TYPE_CHECKING, cast, Literal

from macrobond_data_api.common.enums import StatusCode

from .entity import Entity, EntityColumnsLiterals

SeriesColumnsLiterals = Literal[EntityColumnsLiterals, "Values", "Dates"]

SeriesColumns = List[SeriesColumnsLiterals]

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame
    from .metadata import Metadata
    from .values_metadata import ValuesMetadata

__pdoc__ = {
    "Series.__init__": False,
}


@dataclass(init=False)
class Series(Entity):
    """Represents a Macrobond time series."""

    __slots__ = ("values_metadata", "values", "dates")

    values_metadata: Optional["ValuesMetadata"]
    values: Sequence[Optional[float]]
    dates: Sequence[datetime]

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        status_code: StatusCode,
        metadata: Optional["Metadata"],
        values_metadata: Optional["ValuesMetadata"],
        values: Optional[List[Optional[float]]],
        dates: Optional[List[datetime]],
    ) -> None:
        super().__init__(name, error_message, status_code, metadata)

        self.values_metadata = values_metadata
        """
        The meta data for the values.
        """

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
        """
        The series content as a dictionary of "Name", "Values" and "Dates".
        """
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

    def values_to_pd_data_frame(self) -> "DataFrame":
        """
        A Pandas DataFrame with the with a series called "date" and one called "value"
        """
        import pandas  # pylint: disable=import-outside-toplevel

        if self.is_error:
            ...
        return pandas.DataFrame(
            {
                "date": self.dates,
                "value": self.values,
            }
        )

    def _repr_html_(self) -> str:
        if self.is_error:
            return f"<p>{self.name}</p><p>error_message: {self.error_message}</p>"
        html = self.values_to_pd_data_frame()._repr_html_()
        return f"<p>{self.name}</p>{html}"
