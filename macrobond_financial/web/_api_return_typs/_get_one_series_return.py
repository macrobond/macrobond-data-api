# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import TYPE_CHECKING

from macrobond_financial.common.typs import Series

from macrobond_financial.common.api_return_typs import GetOneSeriesReturn

from ._series_helps import _create_series

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetOneSeriesReturn(GetOneSeriesReturn):
    def __init__(self, session: "Session", series_name: str, _raise: bool) -> None:
        super().__init__(series_name, _raise)
        self._session = session

    def _object(self) -> Series:
        response = self._session.series.fetch_series(self._series_name)[0]
        return _create_series(response, self._series_name)
