from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Sequence, cast

import ijson

from macrobond_data_api.common.types import (
    RevisionInfo,
    GetEntitiesError,
    VintageSeries,
    Series,
    SeriesObservationHistory,
    GetAllVintageSeriesResult,
    SeriesWithVintages,
    VintageValues,
    RevisionHistoryRequest,
    ValuesMetadata,
)
from macrobond_data_api.common.enums import StatusCode
from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601
from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence
from ._split_in_to_chunks import split_in_to_chunks

from .session import ProblemDetailsException, Session

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi
    from .web_types import (
        SeriesWithRevisionsInfoResponse,
        VintageSeriesResponse,
        SeriesWithVintagesResponse,
        RevisionHistoryRequest as WebRevisionHistoryRequest,
        SeriesWithTimesOfChangeResponse,
        VintageValuesResponse,
    )


def _optional_str_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    return _parse_iso8601(datetime_str) if datetime_str else None


def get_revision_info(self: "WebApi", *series_names: str, raise_error: Optional[bool] = None) -> Sequence[RevisionInfo]:
    def to_obj(name: str, serie: "SeriesWithRevisionsInfoResponse") -> RevisionInfo:
        error_text = serie.get("errorText")
        if error_text:
            return RevisionInfo(name, error_text, False, False, None, None, [])

        time_stamp_of_first_revision = _optional_str_to_datetime(serie.get("timeStampOfFirstRevision"))

        time_stamp_of_last_revision = _optional_str_to_datetime(serie.get("timeStampOfLastRevision"))

        stores_revisions = serie["storesRevisions"]

        vintage_time_stamps = [_parse_iso8601(x) for x in serie["vintageTimeStamps"]] if stores_revisions else []

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

    if self.raise_error if raise_error is None else raise_error:
        GetEntitiesError._raise_if([(x, y.get("errorText")) for x, y in zip(series_names, response)])

    return _ReprHtmlSequence([to_obj(x, y) for x, y in zip(series_names, response)])


def get_one_vintage_series(
    self: "WebApi",
    time: datetime,
    series_name: str,
    include_times_of_change: bool = False,
    raise_error: Optional[bool] = None,
) -> VintageSeries:
    return self.get_vintage_series(
        time, [series_name], include_times_of_change=include_times_of_change, raise_error=raise_error
    )[0]


def get_vintage_series(
    self: "WebApi",
    time: datetime,
    series_names: Sequence[str],
    include_times_of_change: bool = False,
    raise_error: Optional[bool] = None,
) -> Sequence[VintageSeries]:
    def to_obj(response: "VintageSeriesResponse", series_name: str) -> VintageSeries:
        error_message = response.get("errorText")
        if error_message:
            return VintageSeries(
                series_name, error_message, StatusCode(cast(int, response["errorCode"])), None, None, None, None, None
            )

        metadata = self.session._create_metadata(response["metadata"])

        values = [float(x) if x is not None else x for x in cast(List[Optional[int]], response["values"])]
        dates = [_parse_iso8601(x) for x in cast(List[str], response["dates"])]

        if include_times_of_change:
            timesOfChange = response.get("timesOfChange")
            if timesOfChange:
                values_metadata = [
                    {"RevisionTimeStamp": _optional_str_to_datetime(x)} for x in cast(List[str], timesOfChange)
                ]
            else:
                values_metadata = [{}] * len(values)
        else:
            values_metadata = None

        vintage_time_stamp = (
            _parse_iso8601(cast(str, response["vintageTimeStamp"])) if "vintageTimeStamp" in response else None
        )

        return VintageSeries(
            series_name, None, StatusCode.OK, metadata, values_metadata, values, dates, vintage_time_stamp
        )

    response = self.session.series.fetch_vintage_series(
        time, *series_names, get_times_of_change=include_times_of_change
    )

    series = [to_obj(x, y) for x, y in zip(response, series_names)]

    if self.raise_error if raise_error is None else raise_error:
        GetEntitiesError._raise_if([(x, y.error_message) for x, y in zip(series_names, series)])

    return _ReprHtmlSequence(series)


def get_one_nth_release(
    self: "WebApi",
    nth: int,
    series_name: str,
    include_times_of_change: bool = False,
    raise_error: Optional[bool] = None,
) -> Series:
    return self.get_nth_release(
        nth, [series_name], include_times_of_change=include_times_of_change, raise_error=raise_error
    )[0]


def get_nth_release(
    self: "WebApi",
    nth: int,
    series_names: Sequence[str],
    include_times_of_change: bool = False,
    raise_error: Optional[bool] = None,
) -> Sequence[Series]:
    def to_obj(response: "SeriesWithTimesOfChangeResponse", name: str, session: Session) -> Series:
        error_text = response.get("errorText")

        if error_text:
            return Series(name, error_text, StatusCode(cast(int, response["errorCode"])), None, None, None, None)

        dates = [_parse_iso8601(x) for x in cast(List[str], response["dates"])]
        values = [float(x) if x is not None else x for x in cast(List[Optional[int]], response["values"])]
        metadata = session._create_metadata(response["metadata"])
        if include_times_of_change:
            timesOfChange = response.get("timesOfChange")
            if not timesOfChange or (len(values) != 0 and _optional_str_to_datetime(timesOfChange[0]) is None):
                values_metadata: Optional[ValuesMetadata] = [{}] * len(values)
            else:
                values_metadata = [
                    {"RevisionTimeStamp": _parse_iso8601(x)} if x else {} for x in cast(List[str], timesOfChange)
                ]
        else:
            values_metadata = None

        return Series(name, "", StatusCode.OK, cast(Dict[str, Any], metadata), values_metadata, values, dates)

    if len(series_names) == 0:
        raise ValueError("No series names")

    response = self.session.series.fetch_nth_release_series(
        nth, *series_names, get_times_of_change=include_times_of_change
    )

    series = [to_obj(x, y, self.session) for x, y in zip(response, series_names)]

    if self.raise_error if raise_error is None else raise_error:
        GetEntitiesError._raise_if([(x, y.error_message) for x, y in zip(series_names, series)])

    return _ReprHtmlSequence(series)


def get_all_vintage_series(self: "WebApi", series_name: str) -> GetAllVintageSeriesResult:
    def to_obj(response: "VintageSeriesResponse", series_name: str) -> VintageSeries:
        error_message = response.get("errorText")
        if error_message:
            return VintageSeries(
                series_name, error_message, StatusCode(cast(int, response["errorCode"])), None, None, None, None, None
            )

        metadata = self.session._create_metadata(response["metadata"])
        values = [float(x) if x is not None else x for x in cast(List[Optional[int]], response["values"])]
        dates = [_parse_iso8601(x) for x in cast(List[str], response["dates"])]

        vintage_time_stamp = (
            _parse_iso8601(cast(str, response["vintageTimeStamp"])) if "vintageTimeStamp" in response else None
        )

        return VintageSeries(series_name, None, StatusCode.OK, metadata, None, values, dates, vintage_time_stamp)

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
                _parse_iso8601(x["observationDate"]),
                [float(y) if y is not None else y for y in x["values"]],
                [_optional_str_to_datetime(y) for y in x["timeStamps"]],
            )
            for x in response
        ]
    )


def _create_vintage_values(vintage_values: "VintageValuesResponse") -> VintageValues:
    _vintage_time_stamp = vintage_values.get("vintageTimeStamp")
    vintage_time_stamp = _parse_iso8601(_vintage_time_stamp) if _vintage_time_stamp else None

    dates = [datetime(int(x[0:4]), int(x[5:7]), int(x[8:10])) for x in vintage_values["dates"]]

    values = [float(x) if x is not None else x for x in vintage_values["values"]]

    return VintageValues(vintage_time_stamp, dates, values)


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
    self: "WebApi", requests: Sequence[RevisionHistoryRequest], include_not_modified: bool = False
) -> Generator[SeriesWithVintages, None, None]:
    if len(requests) == 0:
        yield from ()
    for requests_chunkd in split_in_to_chunks(requests, 200):
        with self.session.series.post_fetch_all_vintage_series(
            _create_web_revision_h_request(requests_chunkd), stream=True
        ) as response:
            self.session.raise_on_error(response)
            ijson_items = ijson.items(self.session._response_to_file_object(response), "item")
            item: "SeriesWithVintagesResponse"
            for item in ijson_items:
                error_code = item.get("errorCode")
                status_code = StatusCode(error_code) if error_code else StatusCode.OK

                if not include_not_modified and status_code == StatusCode.NOT_MODIFIED:
                    continue

                _metadata = item.get("metadata")
                metadata = self.session._create_metadata(_metadata) if _metadata else None

                _vintages = item.get("vintages")
                vintages = [_create_vintage_values(x) for x in _vintages] if _vintages else []

                yield SeriesWithVintages(item.get("errorText"), status_code, metadata, vintages)
