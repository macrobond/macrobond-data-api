# -*- coding: utf-8 -*-

from datetime import datetime

from typing import Any, Dict, Tuple, Optional, List, cast, TYPE_CHECKING
from typing_extensions import Literal

from .entity import Entity, EntityColumnsLiterals

from .._get_pandas import _get_pandas

SeriesColumnsLiterals = Literal[EntityColumnsLiterals, "Values", "Dates"]

SeriesColumns = List[SeriesColumnsLiterals]

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


class Series(Entity):
    """Interface for a Macrobond time series."""

    def __init__(
        self,
        name: str,
        error_message: Optional[str],
        metadata: Optional[Dict[str, Any]],
        values: Optional[Tuple[Optional[float], ...]],
        dates: Optional[Tuple[datetime, ...]],
    ) -> None:
        super().__init__(name, error_message, metadata)
        if values is None:
            self.values: Tuple[Optional[float], ...] = tuple()
            self.dates: Tuple[datetime, ...] = tuple()
        else:
            self.values = values
            self.dates = cast(Tuple[datetime, ...], dates)

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

    def get_values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()

        if self.is_error:
            error_series = {
                "Name": self.name,
                "ErrorMessage": self.error_message,
            }
            kwargs["data"] = [error_series]
        else:
            series = {
                "Values": self.values,
                "Dates": self.dates,
            }

            kwargs["data"] = series

        args = args[1:]
        return pandas.DataFrame(*args, **kwargs)
