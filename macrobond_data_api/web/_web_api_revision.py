# -*- coding: utf-8 -*-

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, cast

from dateutil import parser  # type: ignore

from macrobond_data_api.common.types import (
    RevisionInfo,
    GetEntitiesError,
    VintageSeries,
    Series,
    SeriesObservationHistory,
    GetAllVintageSeriesResult,
)

from .session import ProblemDetailsException, Session

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi

    from .web_types import SeriesWithRevisionsInfoResponse, VintageSeriesResponse

    from .web_types import SeriesResponse


def _optional_str_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    return parser.parse(datetime_str) if datetime_str else None


def _str_to_datetime_no_utc(datetime_str: str) -> datetime:
    return parser.parse(datetime_str, ignoretz=True)


def _create_series(response: "SeriesResponse", name: str, session: Session) -> Series:
    error_text = response.get("errorText")

    if error_text:
        return Series(name, error_text, None, None, None)

    dates = tuple(
        map(
            _str_to_datetime_no_utc,
            cast(List[str], response["dates"]),
        )
    )

    values = tuple(
        map(
            lambda x: float(x) if x else None,
            cast(List[Optional[float]], response["values"]),
        )
    )

    metadata = session._create_metadata(  # pylint: disable=protected-access
        cast(Dict[str, Any], response["metadata"])
    )

    # values = cast(Tuple[Optional[float]], response["values"])
    return Series(name, "", cast(Dict[str, Any], metadata), values, dates)


def get_revision_info(
    self: "WebApi", *series_names: str, raise_error: bool = None
) -> List[RevisionInfo]:
    def to_obj(name: str, serie: "SeriesWithRevisionsInfoResponse"):
        error_text = serie.get("errorText")
        if error_text:
            return RevisionInfo(
                name,
                error_text,
                False,
                False,
                None,
                None,
                tuple(),
            )

        time_stamp_of_first_revision = _optional_str_to_datetime(
            serie.get("timeStampOfFirstRevision")
        )

        time_stamp_of_last_revision = _optional_str_to_datetime(
            serie.get("timeStampOfLastRevision")
        )

        stores_revisions = serie["storesRevisions"]
        if stores_revisions:
            vintage_time_stamps = tuple(
                map(
                    parser.parse,
                    serie["vintageTimeStamps"],
                )
            )
        else:
            vintage_time_stamps = tuple()

        return RevisionInfo(
            name,
            "",
            stores_revisions,
            serie["hasRevisions"],
            time_stamp_of_first_revision,
            time_stamp_of_last_revision,
            vintage_time_stamps,
        )

    response = self.session.series.get_revision_info(*series_names)

    GetEntitiesError.raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.get("errorText")), series_names, response),
    )

    return list(map(to_obj, series_names, response))


def get_vintage_series(
    self: "WebApi", time: datetime, *series_names: str, raise_error: bool = None
) -> List[VintageSeries]:
    def to_obj(response: "VintageSeriesResponse", series_name: str) -> VintageSeries:
        error_message = response.get("errorText")
        if error_message:
            return VintageSeries(series_name, error_message, None, None, None)

        metadata = self.session._create_metadata(  # pylint: disable=protected-access
            cast(Dict[str, Any], response["metadata"])
        )

        revision_time_stamp = cast(str, metadata.get("RevisionTimeStamp"))

        if not revision_time_stamp or time != revision_time_stamp:
            raise ValueError("Invalid time")

        values: Tuple[Optional[float], ...] = tuple(
            map(
                lambda x: float(x) if x else None,
                cast(List[Optional[float]], response["values"]),
            )
        )

        dates = tuple(map(_str_to_datetime_no_utc, cast(List[str], response["dates"])))

        return VintageSeries(series_name, None, metadata, values, dates)

    response = self.session.series.fetch_vintage_series(
        time, *series_names, get_times_of_change=False
    )

    series = list(map(to_obj, response, series_names))

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
    self: "WebApi", nth: int, *series_names: str, raise_error: bool = None
) -> List[Series]:
    response = self.session.series.fetch_nth_release_series(nth, *series_names)

    series = list(map(lambda x, y: _create_series(x, y, self.session), response, series_names))

    GetEntitiesError.raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(
            lambda x, y: (x, y.error_message if y.is_error else None),
            series_names,
            series,
        ),
    )

    return series


def get_all_vintage_series(self: "WebApi", series_name: str) -> GetAllVintageSeriesResult:
    try:
        response = self.session.series.get_fetch_all_vintage_series(series_name)
    except ProblemDetailsException as ex:
        if ex.status == 404:
            raise ValueError("Series not found: " + series_name) from ex
        raise ex

    return GetAllVintageSeriesResult(
        list(map(lambda x: _create_series(x, series_name, self.session), response)), series_name
    )


def get_observation_history(
    self: "WebApi", serie_name: str, *times: datetime
) -> List[SeriesObservationHistory]:
    try:
        response = self.session.series.fetch_observation_history(serie_name, list(times))
    except ProblemDetailsException as ex:
        if ex.status == 404:
            raise Exception(ex.detail) from ex
        raise ex

    return list(
        map(
            lambda x: SeriesObservationHistory(
                parser.parse(x["observationDate"]),
                tuple(map(lambda v: float(v) if v else None, x["values"])),
                tuple(map(parser.parser, x["timeStamps"])),
            ),
            response,
        )
    )
