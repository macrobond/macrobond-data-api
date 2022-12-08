# -*- coding: utf-8 -*-

from math import isnan
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING, Sequence

from datetime import datetime, timezone

from macrobond_data_api.common.types import (
    RevisionInfo,
    GetEntitiesError,
    VintageSeries,
    Series,
    GetAllVintageSeriesResult,
    SeriesObservationHistory,
)

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from .com_types import SeriesWithRevisions

    from .com_types import Series as ComSeries, Entity as ComEntity


def _fill_metadata_from_entity(com_entity: "ComEntity") -> Dict[str, Any]:
    ret = {}
    metadata = com_entity.Metadata

    for names_and_description in metadata.ListNames():
        name = names_and_description[0]
        values = metadata.GetValues(name)
        ret[name] = values[0] if len(values) == 1 else list(values)

    if "FullDescription" not in ret:
        ret["FullDescription"] = com_entity.Title

    return ret


def _datetime_to_datetime_utc(dates: Sequence[datetime]) -> Tuple[datetime, ...]:
    return tuple(
        map(
            lambda x: datetime(
                x.year,
                x.month,
                x.day,
                x.hour,
                x.minute,
                x.second,
                x.microsecond,
                timezone.utc,
            ),
            dates,
        )
    )


def _datetime_to_datetime(dates: Sequence[datetime]) -> Tuple[datetime, ...]:
    return tuple(
        map(
            lambda x: datetime(
                x.year,
                x.month,
                x.day,
                x.hour,
                x.minute,
                x.second,
                x.microsecond,
            ),
            dates,
        )
    )


def _remove_padding(
    series: "ComSeries",
) -> Tuple[Tuple[Optional[float], ...], Tuple[datetime, ...]]:
    series_values = series.Values

    padding_front = 0
    for value in series_values:
        if value is None or not isnan(value):
            break
        padding_front = padding_front + 1

    padding_back = 0
    for value in series_values[::-1]:
        if value is None or not isnan(value):
            break
        padding_back = padding_back + 1

    padding_back = len(series_values) - padding_back

    return (
        tuple(series_values[padding_front:padding_back]),
        # _datetime_to_datetime(
        series.DatesAtStartOfPeriod[padding_front:padding_back]
        # ),
    )


def get_revision_info(
    self: "ComApi", *series_names: str, raise_error: bool = None
) -> List[RevisionInfo]:
    def to_obj(name: str, serie: "SeriesWithRevisions"):
        if serie.IsError:
            return RevisionInfo(
                name,
                serie.ErrorMessage,
                False,
                False,
                None,
                None,
                tuple(),
            )

        vintage_time_stamps = _datetime_to_datetime_utc(serie.GetVintageDates())

        time_stamp_of_first_revision = vintage_time_stamps[0] if serie.HasRevisions else None
        time_stamp_of_last_revision = vintage_time_stamps[-1] if serie.HasRevisions else None

        return RevisionInfo(
            name,
            "",
            serie.StoresRevisions,
            serie.HasRevisions,
            time_stamp_of_first_revision,
            time_stamp_of_last_revision,
            vintage_time_stamps,
        )

    series = self.database.FetchSeriesWithRevisions(series_names)

    GetEntitiesError.raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(
            lambda x, y: (x, y.ErrorMessage if y.IsError else None),
            series_names,
            series,
        ),
    )

    return list(map(to_obj, series_names, series))


def get_vintage_series(
    self: "ComApi", time: datetime, *series_names: str, raise_error: bool = None
) -> List[VintageSeries]:
    def to_obj(series_name: str) -> VintageSeries:
        series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

        if series_with_revisions.IsError:
            return VintageSeries(
                series_name,
                series_with_revisions.ErrorMessage,
                None,
                None,
                None,
            )

        try:
            series = series_with_revisions.GetVintage(time)
        except OSError as os_error:
            if os_error.errno == 22 and os_error.strerror == "Invalid argument":
                raise ValueError("Invalid time") from os_error
            raise os_error

        if series.IsError:
            return VintageSeries(
                series_name,
                series.ErrorMessage,
                None,
                None,
                None,
            )

        values_and_dates = _remove_padding(series)

        return VintageSeries(
            series_name,
            "",
            _fill_metadata_from_entity(series),
            values_and_dates[0],
            _datetime_to_datetime(values_and_dates[1]),
        )

    series = list(map(to_obj, series_names))

    GetEntitiesError.raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(
            lambda x, y: (x, y.error_message if y.is_error else None),
            series_names,
            series,
        ),
    )

    return series


def get_nth_release(
    self: "ComApi", nth: int, *series_names: str, raise_error: bool = None
) -> List[Series]:
    def to_obj(series_name: str) -> Series:
        series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

        if series_with_revisions.IsError:
            return Series(
                series_name,
                series_with_revisions.ErrorMessage,
                None,
                None,
                None,
            )

        series = series_with_revisions.GetNthRelease(nth)
        if series.IsError:
            return Series(
                series_name,
                series.ErrorMessage,
                None,
                None,
                None,
            )

        values = tuple(map(lambda x: None if isnan(x) else x, series.Values))  # type: ignore

        dates = _datetime_to_datetime(series.DatesAtStartOfPeriod)

        return Series(
            series_name,
            None,
            _fill_metadata_from_entity(series),
            values,
            dates,
        )

    series = list(map(to_obj, series_names))

    GetEntitiesError.raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(
            lambda x, y: (x, y.error_message if y.is_error else None),
            series_names,
            series,
        ),
    )

    return series


def get_all_vintage_series(self: "ComApi", series_name: str) -> GetAllVintageSeriesResult:
    def to_obj(com_series: "ComSeries", name: str):
        if com_series.IsError:
            return Series(name, com_series.ErrorMessage, None, None, None)

        values_and_dates = _remove_padding(com_series)

        return Series(
            name,
            None,
            _fill_metadata_from_entity(com_series),
            values_and_dates[0],
            _datetime_to_datetime(values_and_dates[1]),
        )

    series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

    if series_with_revisions.IsError:
        if series_with_revisions.ErrorMessage == "Not found":
            raise ValueError("Series not found: " + series_name)
        raise Exception(series_with_revisions.ErrorMessage)

    return GetAllVintageSeriesResult(
        list(
            map(
                lambda x: to_obj(x, series_name),
                series_with_revisions.GetCompleteHistory(),
            )
        ),
        series_name,
    )


def get_observation_history(
    self: "ComApi", serie_name: str, *times: datetime
) -> List[SeriesObservationHistory]:

    series_with_revisions = self.database.FetchOneSeriesWithRevisions(serie_name)

    if series_with_revisions.IsError:
        if series_with_revisions.ErrorMessage == "Not found":
            raise ValueError("Not found " + serie_name)
        raise Exception(series_with_revisions.ErrorMessage)

    def to_obj(time: datetime) -> SeriesObservationHistory:
        series = series_with_revisions.GetObservationHistory(time)
        dates = _datetime_to_datetime(series.DatesAtStartOfPeriod)
        return SeriesObservationHistory(time, series.Values, dates)

    return list(map(to_obj, times))
