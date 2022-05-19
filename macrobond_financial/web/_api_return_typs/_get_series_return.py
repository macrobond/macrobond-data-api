# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Tuple, List, TYPE_CHECKING
from macrobond_financial.common.typs import Series

from macrobond_financial.common.api_return_typs import GetSeriesReturn

from ._series_helps import _create_series

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetSeriesReturn(GetSeriesReturn):
    def __init__(
        self, session: "Session", series_names: Tuple[str, ...], _raise: bool
    ) -> None:
        super().__init__(series_names, _raise)
        self._session = session

    def _list_of_objects(self) -> List[Series]:
        response = self._session.series.fetch_series(*self._series_names)
        return list(map(_create_series, response, self._series_names))
