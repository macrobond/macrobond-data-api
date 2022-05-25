# -*- coding: utf-8 -*-

from typing import Tuple, List, TYPE_CHECKING

from macrobond_financial.common.types import Series
from macrobond_financial.common.api_return_types import GetSeriesReturn

from ._series_helps import _create_series

if TYPE_CHECKING:  # pragma: no cover
    from ..com_types import Database


class _GetSeriesReturn(GetSeriesReturn):
    def __init__(
        self, database: "Database", series_names: Tuple[str, ...], _raise: bool
    ) -> None:
        super().__init__(series_names, _raise)
        self._database = database

    def _list_of_objects(self) -> List[Series]:
        series = self._database.FetchSeries(self._series_names)
        return list(map(_create_series, series, self._series_names))