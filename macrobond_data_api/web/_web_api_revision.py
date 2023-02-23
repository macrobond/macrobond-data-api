from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Sequence, TypeVar, cast

from dateutil import parser

import ijson  # type: ignore

from macrobond_data_api.common.types import (
    RevisionInfo,
    GetEntitiesError,
    VintageSeries,
    Series,
    SeriesObservationHistory,
    GetAllVintageSeriesResult,
    SeriesWithVintages,
    VintageValues,
    SeriesWithVintagesErrorCode,
    RevisionHistoryRequest,
)
from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence

from .session import ProblemDetailsException, Session, _raise_on_error

# from .series_with_vintages import SeriesWithVintages


if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi

    from .web_types import (
        SeriesWithRevisionsInfoResponse,
        VintageSeriesResponse,
        SeriesWithVintagesResponse,
        RevisionHistoryRequest as WebRevisionHistoryRequest,
        SeriesResponse,
        VintageValuesResponse,
    )


def _optional_str_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    return parser.parse(datetime_str) if datetime_str else None


def _str_to_datetime_ignoretz(datetime_str: str) -> datetime:
    return parser.parse(datetime_str, ignoretz=True)


def _str_to_datetime(datetime_str: str) -> datetime:
    return parser.parse(datetime_str)


def _optional_str_to_datetime_ignoretz(datetime_str: Optional[str]) -> Optional[datetime]:
    return parser.parse(datetime_str, ignoretz=True) if datetime_str else None


def int_to_float_or_none(int_: Optional[int]) -> Optional[float]:
    return float(int_) if int_ else None


def _create_series(response: "SeriesResponse", name: str, session: Session) -> Series:
    error_text = response.get("errorText")

    if error_text:
        return Series(name, error_text, None, None, None)

    dates = [_str_to_datetime_ignoretz(x) for x in cast(List[str], response["dates"])]
    values = [float(x) if x else None for x in cast(List[Optional[int]], response["values"])]
    metadata = session._create_metadata(response["metadata"])

    return Series(name, "", cast(Dict[str, Any], metadata), values, dates)


def get_revision_info(self: "WebApi", *series_names: str, raise_error: Optional[bool] = None) -> Sequence[RevisionInfo]:
    def to_obj(name: str, serie: "SeriesWithRevisionsInfoResponse") -> RevisionInfo:
        error_text = serie.get("errorText")
        if error_text:
            return RevisionInfo(name, error_text, False, False, None, None, [])

        time_stamp_of_first_revision = _optional_str_to_datetime(serie.get("timeStampOfFirstRevision"))

        time_stamp_of_last_revision = _optional_str_to_datetime(serie.get("timeStampOfLastRevision"))

        stores_revisions = serie["storesRevisions"]

        vintage_time_stamps = [parser.parse(x) for x in serie["vintageTimeStamps"]] if stores_revisions else []

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

    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.get("errorText")), series_names, response),
    )

    return _ReprHtmlSequence([to_obj(x, y) for x, y in zip(series_names, response)])


def get_vintage_series(
    self: "WebApi", time: datetime, *series_names: str, raise_error: Optional[bool] = None
) -> Sequence[VintageSeries]:
    def to_obj(response: "VintageSeriesResponse", series_name: str) -> VintageSeries:
        error_message = response.get("errorText")
        if error_message:
            return VintageSeries(series_name, error_message, None, None, None, None)

        metadata = self.session._create_metadata(response["metadata"])

        revision_time_stamp = cast(str, metadata.get("RevisionTimeStamp"))

        if not revision_time_stamp or time != revision_time_stamp:
            raise ValueError("Invalid time")

        values = [float(x) if x else None for x in cast(List[Optional[int]], response["values"])]
        dates = [_str_to_datetime_ignoretz(x) for x in cast(List[str], response["dates"])]

        vintage_time_stamp = (
            _str_to_datetime(cast(str, response["vintageTimeStamp"])) if "vintageTimeStamp" in response else None
        )

        return VintageSeries(series_name, None, metadata, values, dates, vintage_time_stamp)

    response = self.session.series.fetch_vintage_series(time, *series_names, get_times_of_change=False)

    series = [to_obj(x, y) for x, y in zip(response, series_names)]

    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.error_message if y.is_error else None), series_names, series),
    )

    return _ReprHtmlSequence(series)


def get_nth_release(
    self: "WebApi", nth: int, *series_names: str, raise_error: Optional[bool] = None
) -> Sequence[Series]:
    response = self.session.series.fetch_nth_release_series(nth, *series_names)

    series = [_create_series(x, y, self.session) for x, y in zip(response, series_names)]

    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.error_message if y.is_error else None), series_names, series),
    )

    return _ReprHtmlSequence(series)


def get_all_vintage_series(self: "WebApi", series_name: str) -> GetAllVintageSeriesResult:
    def to_obj(response: "VintageSeriesResponse", series_name: str) -> VintageSeries:
        error_message = response.get("errorText")
        if error_message:
            return VintageSeries(series_name, error_message, None, None, None, None)

        metadata = self.session._create_metadata(response["metadata"])
        values = [float(x) if x else None for x in cast(List[Optional[int]], response["values"])]
        dates = [_str_to_datetime_ignoretz(x) for x in cast(List[str], response["dates"])]

        vintage_time_stamp = (
            _str_to_datetime(cast(str, response["vintageTimeStamp"])) if "vintageTimeStamp" in response else None
        )

        return VintageSeries(series_name, None, metadata, values, dates, vintage_time_stamp)

    try:
        response = self.session.series.get_fetch_all_vintage_series(series_name)
    except ProblemDetailsException as ex:
        if ex.status == 404:
            raise ValueError("Series not found: " + series_name) from ex
        raise ex

    return GetAllVintageSeriesResult([to_obj(x, series_name) for x in response], series_name)


def get_observation_history(self: "WebApi", series_name: str, *times: datetime) -> Sequence[SeriesObservationHistory]:
    try:
        response = self.session.series.fetch_observation_history(series_name, list(times))
    except ProblemDetailsException as ex:
        if ex.status == 404:
            raise Exception(ex.detail) from ex
        raise ex

    return _ReprHtmlSequence(
        [
            SeriesObservationHistory(
                parser.parse(x["observationDate"]),
                [float(y) if y else None for y in x["values"]],
                [_optional_str_to_datetime_ignoretz(y) for y in x["timeStamps"]],
            )
            for x in response
        ]
    )


def _create_vintage_values(vintage_values: "VintageValuesResponse") -> VintageValues:
    _vintage_time_stamp = vintage_values.get("vintageTimeStamp")
    vintage_time_stamp = parser.parse(_vintage_time_stamp) if _vintage_time_stamp else None

    dates = [datetime(int(x[0:4]), int(x[5:7]), int(x[8:10])) for x in vintage_values["dates"]]

    values = [float(x) if x else None for x in vintage_values["values"]]

    return VintageValues(vintage_time_stamp, dates, values)


SplitInToChunksTypeVar = TypeVar("SplitInToChunksTypeVar")


def _split_in_to_chunks(
    sequence: Sequence[SplitInToChunksTypeVar], chunk_size: int
) -> Generator[Sequence[SplitInToChunksTypeVar], None, None]:
    for i in range(0, len(sequence), chunk_size):
        yield sequence[i : i + chunk_size]


def _create_web_revision_h_request(requests: Sequence[RevisionHistoryRequest]) -> List["WebRevisionHistoryRequest"]:
    return [
        {
            "name": x.name,
            "ifModifiedSince": x.if_modified_since.isoformat() if x.if_modified_since else None,
            "lastRevision": x.last_revision.isoformat().replace("+00:00", "Z") if x.last_revision else None,
            "lastRevisionAdjustment": x.last_revision_adjustment.isoformat().replace("+00:00", "Z")
            if x.last_revision_adjustment
            else None,
        }
        for x in requests
    ]


def get_many_series_with_revisions(
    self: "WebApi",
    requests: Sequence[RevisionHistoryRequest],
) -> Generator[SeriesWithVintages, None, None]:
    if len(requests) == 0:
        yield from ()
    for requests_chunkd in _split_in_to_chunks(requests, 200):
        with self.session.series.post_fetch_all_vintage_series(
            _create_web_revision_h_request(requests_chunkd), stream=True
        ) as response:
            _raise_on_error(response)
            ijson_items = ijson.items(response.raw, "item")
            item: "SeriesWithVintagesResponse"
            for item in ijson_items:
                _error_code = item.get("errorCode")
                error_code = SeriesWithVintagesErrorCode(_error_code) if _error_code else None

                _metadata = item.get("metadata")
                metadata = self.session._create_metadata(_metadata) if _metadata else None

                _vintages = item.get("vintages")
                vintages = [_create_vintage_values(x) for x in _vintages] if _vintages else []

                yield SeriesWithVintages(item.get("errorText"), error_code, metadata, vintages)
