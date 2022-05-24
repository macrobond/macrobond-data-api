# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from math import isnan

from macrobond_financial.common.api_return_typs import GetNthReleaseReturn

from macrobond_financial.common.types import Series

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database


class _GetNthReleaseReturn(GetNthReleaseReturn):
    def __init__(
        self,
        database: "Database",
        series_name: str,
        nth: int,
        _raise: bool,
    ) -> None:
        super().__init__(series_name, nth, _raise)
        self._database = database

    def _object(self) -> Series:
        series_with_revisions = self._database.FetchOneSeriesWithRevisions(
            self._series_name
        )

        if series_with_revisions.IsError:
            return Series(
                self._series_name,
                series_with_revisions.ErrorMessage,
                None,
                None,
                None,
            )

        series = series_with_revisions.GetNthRelease(self._nth)
        if series.IsError:
            return Series(
                self._series_name,
                series.ErrorMessage,
                None,
                None,
                None,
            )

        values = tuple(
            map(lambda x: None if isnan(x) else x, series.Values)  # type: ignore
        )

        return Series(
            self._series_name,
            None,
            _fill_metadata_from_entity(series),
            values,
            series.DatesAtStartOfPeriod,
        )
