# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_financial.common.types import Series

from macrobond_financial.common.api_return_typs import GetOneSeriesReturn

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database


class _GetOneSeriesReturn(GetOneSeriesReturn):
    def __init__(self, database: "Database", series_name: str, _raise: bool) -> None:
        super().__init__(series_name, _raise)
        self.__database = database

    def _object(self) -> Series:
        series = self.__database.FetchOneSeries(self._series_name)
        if series.IsError:
            return Series(self._series_name, series.ErrorMessage, None, None, None)
        return Series(
            self._series_name,
            None,
            _fill_metadata_from_entity(series),
            series.Values,
            series.DatesAtStartOfPeriod,
        )
