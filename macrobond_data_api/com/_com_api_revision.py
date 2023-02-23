from math import isnan
from typing import Generator, Optional, Tuple, List, TYPE_CHECKING, Sequence, cast

from datetime import datetime, timezone
from dateutil.tz import tzutc

from macrobond_data_api.common.types import (
    RevisionInfo,
    GetEntitiesError,
    VintageSeries,
    Series,
    GetAllVintageSeriesResult,
    SeriesObservationHistory,
    SeriesWithVintages,
    SeriesWithVintagesErrorCode,
    RevisionHistoryRequest,
    VintageValues,
)

from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from .com_types import SeriesWithRevisions

    from .com_types import Series as ComSeries, Entity as ComEntity


def _datetime_to_datetime_utc(dates: Sequence[datetime]) -> List[datetime]:
    return [datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond, timezone.utc) for x in dates]


def _datetime_to_datetime_timezone(dates: Sequence[datetime]) -> List[datetime]:
    return [datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond) for x in dates]


def _remove_padding(
    series: "ComSeries",
) -> Tuple[List[Optional[float]], Tuple[datetime, ...]]:
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

    return (list(series_values[padding_front:padding_back]), series.DatesAtStartOfPeriod[padding_front:padding_back])


def get_revision_info(self: "ComApi", *series_names: str, raise_error: bool = None) -> Sequence[RevisionInfo]:
    def to_obj(name: str, serie: "SeriesWithRevisions") -> RevisionInfo:
        if serie.IsError:
            return RevisionInfo(name, serie.ErrorMessage, False, False, None, None, [])

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

    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.ErrorMessage if y.IsError else None), series_names, series),
    )

    return _ReprHtmlSequence([to_obj(x, y) for x, y in zip(series_names, series)])


def get_vintage_series(
    self: "ComApi", time: datetime, *series_names: str, raise_error: bool = None
) -> Sequence[VintageSeries]:
    def to_obj(series_name: str) -> VintageSeries:
        series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

        if series_with_revisions.IsError:
            return VintageSeries(series_name, series_with_revisions.ErrorMessage, None, None, None, None)

        try:
            series = series_with_revisions.GetVintage(time)
        except OSError as os_error:
            if os_error.errno == 22 and os_error.strerror == "Invalid argument":
                raise ValueError("Invalid time") from os_error
            raise os_error

        if series.IsError:
            return VintageSeries(series_name, series.ErrorMessage, None, None, None, None)

        values, dates = _remove_padding(series)

        return VintageSeries(
            series_name, "", _fill_metadata_from_entity(series), values, _datetime_to_datetime_timezone(dates), None
        )

    series = [to_obj(x) for x in series_names]

    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.error_message if y.is_error else None), series_names, series),
    )

    return _ReprHtmlSequence(series)


def get_nth_release(self: "ComApi", nth: int, *series_names: str, raise_error: bool = None) -> Sequence[Series]:
    def to_obj(series_name: str) -> Series:
        series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

        if series_with_revisions.IsError:
            return Series(series_name, series_with_revisions.ErrorMessage, None, None, None)

        series = series_with_revisions.GetNthRelease(nth)
        if series.IsError:
            return Series(series_name, series.ErrorMessage, None, None, None)

        values = [None if isnan(x) else x for x in series.Values]  # type: ignore

        dates = _datetime_to_datetime_timezone(series.DatesAtStartOfPeriod)

        return Series(series_name, None, _fill_metadata_from_entity(series), values, dates)

    series = [to_obj(x) for x in series_names]

    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.error_message if y.is_error else None), series_names, series),
    )

    return _ReprHtmlSequence(series)


def get_all_vintage_series(self: "ComApi", series_name: str) -> GetAllVintageSeriesResult:
    def to_obj(com_series: "ComSeries", name: str) -> VintageSeries:
        if com_series.IsError:
            return VintageSeries(name, com_series.ErrorMessage, None, None, None, None)

        values, dates = _remove_padding(com_series)

        return VintageSeries(
            name, None, _fill_metadata_from_entity(com_series), values, _datetime_to_datetime_timezone(dates), None
        )

    series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

    if series_with_revisions.IsError:
        if series_with_revisions.ErrorMessage == "Not found":
            raise ValueError("Series not found: " + series_name)
        raise Exception(series_with_revisions.ErrorMessage)

    return GetAllVintageSeriesResult(
        [to_obj(x, series_name) for x in series_with_revisions.GetCompleteHistory()],
        series_name,
    )


def get_observation_history(self: "ComApi", series_name: str, *times: datetime) -> Sequence[SeriesObservationHistory]:
    series_with_revisions = self.database.FetchOneSeriesWithRevisions(series_name)

    if series_with_revisions.IsError:
        if series_with_revisions.ErrorMessage == "Not found":
            raise ValueError("Not found " + series_name)
        raise Exception(series_with_revisions.ErrorMessage)

    def to_obj(time: datetime) -> SeriesObservationHistory:
        series = series_with_revisions.GetObservationHistory(time)
        dates = _datetime_to_datetime_timezone(series.DatesAtStartOfPeriod)
        return SeriesObservationHistory(time, series.Values, dates)

    return _ReprHtmlSequence([to_obj(x) for x in times])


def _create_vintage_values(
    start_index: int, vintage_dates: List[datetime], com_series: List["ComSeries"]
) -> Generator[VintageValues, None, None]:
    if start_index == 0:
        values, dates = _remove_padding(com_series[0])
        yield VintageValues(None, _datetime_to_datetime_timezone(dates), values)

    for vintage_date, series in zip(vintage_dates[start_index:], com_series[start_index + 1 :]):
        vintage_date = datetime(
            vintage_date.year,
            vintage_date.month,
            vintage_date.day,
            vintage_date.hour,
            vintage_date.minute,
            vintage_date.second,
            vintage_date.microsecond,
            tzutc(),
        )
        values, dates = _remove_padding(series)
        yield VintageValues(vintage_date, _datetime_to_datetime_timezone(dates), values)


def _equal_with_margin(d1: Optional[datetime], d2: Optional[datetime]) -> bool:
    if not d1 and not d2:
        return True

    if not d1 or not d2:
        return False

    return abs((d2 - d1).total_seconds()) < 0.5


def _less_than_or_equal_with_margin(d1: Optional[datetime], d2: Optional[datetime]) -> bool:
    if not d1 and not d2:
        return True

    if not d1 or not d2:
        return False

    return (d1 - d2).total_seconds() < 0.5


def get_many_series_with_revisions(
    self: "ComApi", requests: Sequence[RevisionHistoryRequest]
) -> Generator[SeriesWithVintages, None, None]:
    if len(requests) == 0:
        yield from ()

    for request in requests:
        series_with_revisions = self.database.FetchOneSeriesWithRevisions(request.name)

        if series_with_revisions.IsError:
            if series_with_revisions.ErrorMessage == "Not found":
                yield SeriesWithVintages("Not Found", SeriesWithVintagesErrorCode.NOT_FOUND, None, [])
                continue
            raise Exception(series_with_revisions.ErrorMessage)

        head = series_with_revisions.Head
        metadata = _fill_metadata_from_entity(head)
        last_revision_adjustment = metadata["LastRevisionAdjustmentTimeStamp"]
        # last_revision_time = metadata["LastRevisionTimeStamp"]
        last_modified_time = metadata["LastModifiedTimeStamp"]

        if (
            request.if_modified_since
            and last_modified_time
            and _less_than_or_equal_with_margin(last_modified_time, request.if_modified_since)
        ):
            yield SeriesWithVintages("Not modified", SeriesWithVintagesErrorCode.NOT_MODIFIED, None, [])
            continue

        can_do_incremental_response = request.last_revision is not None

        if can_do_incremental_response and not request.if_modified_since:
            yield SeriesWithVintages(
                "If lastRevision is specified, then ifModifiedSince must also be included",
                SeriesWithVintagesErrorCode.OTHER,
                None,
                [],
            )
            continue

        if (
            can_do_incremental_response
            and last_revision_adjustment
            and not _equal_with_margin(request.last_revision_adjustment, last_revision_adjustment)
        ):
            can_do_incremental_response = False

        vintage_dates = series_with_revisions.GetVintageDates()
        complete_history = series_with_revisions.GetCompleteHistory()

        if can_do_incremental_response:
            request_last_revision = cast(datetime, request.last_revision)
            index = -1
            for i, vintage_date in enumerate(vintage_dates):
                if (
                    vintage_date.year == request_last_revision.year
                    and vintage_date.month == request_last_revision.month
                    and vintage_date.day == request_last_revision.day
                    and vintage_date.hour == request_last_revision.hour
                    and vintage_date.minute == request_last_revision.minute
                ):
                    index = i + 1
                    break

            if index != -1:
                yield SeriesWithVintages(
                    "Incremental update",
                    SeriesWithVintagesErrorCode.PARTIAL_CONTENT,
                    metadata,
                    list(_create_vintage_values(index, vintage_dates, complete_history)),
                )
                continue
        yield SeriesWithVintages(
            None,
            None,
            metadata,
            list(_create_vintage_values(0, vintage_dates, complete_history)),
        )
