# -*- coding: utf-8 -*-

from typing import Any, Dict, Tuple, Optional, List, Union, cast, TYPE_CHECKING

from datetime import datetime

from .entity import Entity

# from ._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore

    from .entity import EntityColumnsLiterals, ErrorEntityTypedDict, EntityTypedDict

    from typing_extensions import Literal

    SeriesColumns = List[Literal[EntityColumnsLiterals, "Values", "Dates"]]

    class ErrorSeriesTypedDict(ErrorEntityTypedDict):
        ...

    class SeriesTypedDict(EntityTypedDict):
        Values: Tuple[Optional[float], ...]
        Dates: Tuple[datetime, ...]

    SeriesTypedDicts = Union[SeriesTypedDict, ErrorSeriesTypedDict]


class Series(Entity):
    """Interface for a Macrobond time series."""

    def __init__(
        self,
        error_message: str,
        metadata: Dict[str, Any],
        values: Optional[Tuple[Optional[float], ...]],
        dates: Optional[Tuple[datetime, ...]],
    ) -> None:
        super().__init__(error_message, metadata)
        if values is None:
            self.values: Tuple[Optional[float], ...] = tuple()
            self.dates: Tuple[datetime, ...] = tuple()
        else:
            self.values = values
            self.dates = cast(Tuple[datetime, ...], dates)

    def get_values_and_dates_as_data_frame(self) -> "DataFrame":
        raise NotImplementedError()
        # metadata = self.metadata
        # pandas = _get_pandas()
        # return pandas.DataFrame.from_dict(
        #     metadata, orient='index', columns=['Attributes']
        # )
