# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from datetime import datetime

from math import isnan

from macrobond_financial.common.api_return_types import GetVintageSeriesReturn

from macrobond_financial.common.types import VintageSeries

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from ..com_types import Database, Series as ComSeries


class _GetVintageSeriesReturn(GetVintageSeriesReturn):
    def __init__(
        self,
        database: "Database",
        serie_name: str,
        time: datetime,
        _raise: bool,
    ) -> None:
        super().__init__(serie_name, time, _raise)
        self._database = database

    def _object(self) -> VintageSeries:
        series_with_revisions = self._database.FetchOneSeriesWithRevisions(
            self._serie_name
        )

        if series_with_revisions.IsError:
            return VintageSeries(
                self._serie_name,
                series_with_revisions.ErrorMessage,
                None,
                None,
                None,
            )

        try:
            series = series_with_revisions.GetVintage(self._time)
        except OSError as os_error:
            if os_error.errno == 22 and os_error.strerror == "Invalid argument":
                raise ValueError("Invalid time") from os_error
            raise os_error

        if series.IsError:
            return VintageSeries(
                self._serie_name,
                series.ErrorMessage,
                None,
                None,
                None,
            )

        # series = cast("ComSeries", series)

        values = tuple(filter(lambda x: x is not None and not isnan(x), series.Values))
        dates = series.DatesAtStartOfPeriod[: len(values)]

        return VintageSeries(
            self._serie_name,
            "",
            _fill_metadata_from_entity(series),
            values,
            dates,
        )
