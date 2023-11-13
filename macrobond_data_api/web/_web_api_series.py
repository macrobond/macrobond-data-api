from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Sequence, Tuple, Union, cast

from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence
from macrobond_data_api.common.types._parse_iso8601 import _parse_iso8601

from macrobond_data_api.common.enums import SeriesWeekdays, SeriesFrequency, CalendarMergeMode, StatusCode
from macrobond_data_api.common.types import (
    GetEntitiesError,
    EntityErrorInfo,
    Series,
    Entity,
    UnifiedSeries,
    UnifiedSeriesList,
    SeriesEntry,
)

from .session import Session
from ._split_in_to_chunks import split_in_to_chunks

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi

    from macrobond_data_api.common.types import StartOrEndPoint

    from .web_types import UnifiedSeriesRequest, UnifiedSeriesEntry, EntityRequest

    from .web_types import SeriesResponse, EntityResponse


__pdoc__ = {
    "WebApi.__init__": False,
}


def _create_entity(response: "EntityResponse", name: str, session: Session) -> Entity:
    error_text = response.get("errorText")

    if error_text:
        return Entity(name, error_text, StatusCode(cast(int, response["errorCode"])), None)

    metadata = session._create_metadata(response["metadata"])

    return Entity(name, None, StatusCode.OK, cast(Dict[str, Any], metadata))


def _create_series(response: "SeriesResponse", name: str, session: Session) -> Series:
    error_text = response.get("errorText")

    if error_text:
        return Series(name, error_text, StatusCode(cast(int, response["errorCode"])), None, None, None, None)

    dates = [_parse_iso8601(x) for x in cast(List[str], response["dates"])]

    values = [float(x) if x is not None else x for x in cast(List[Optional[float]], response["values"])]

    metadata = session._create_metadata(response["metadata"])

    # values = cast(Tuple[Optional[float]], response["values"])
    return Series(name, "", StatusCode.OK, metadata, None, values, dates)


def get_one_series(self: "WebApi", series_name: str, raise_error: Optional[bool] = None) -> Series:
    return self.get_series([series_name], raise_error=raise_error)[0]


def get_series(self: "WebApi", series_names: Sequence[str], raise_error: Optional[bool] = None) -> Sequence[Series]:
    response = self.session.series.get_fetch_series(*series_names)
    series = [_create_series(x, y, self.session) for x, y in zip(response, series_names)]
    if self.raise_error if raise_error is None else raise_error:
        GetEntitiesError._raise_if([(x, y.error_message) for x, y in zip(series_names, series)])
    return _ReprHtmlSequence(series)


def get_one_entity(self: "WebApi", entity_name: str, raise_error: Optional[bool] = None) -> Entity:
    return self.get_entities([entity_name], raise_error=raise_error)[0]


def get_entities(self: "WebApi", entity_names: Sequence[str], raise_error: Optional[bool] = None) -> Sequence[Entity]:
    response = self.session.series.fetch_entities(*entity_names)
    entitys = [_create_entity(x, y, self.session) for x, y in zip(response, entity_names)]
    if self.raise_error if raise_error is None else raise_error:
        GetEntitiesError._raise_if([(x, y.error_message) for x, y in zip(entity_names, entitys)])
    return _ReprHtmlSequence(entitys)


def get_many_series(
    self: "WebApi", series: Sequence[Union[str, Tuple[str, Optional[datetime]]]], include_not_modified: bool = False
) -> Generator[Series, None, None]:
    if len(series) == 0:
        yield from ()

    series_as_tuple: List[Tuple[str, Optional[datetime]]] = [(x, None) if isinstance(x, str) else x for x in series]

    names = {x[0] for x in series_as_tuple}

    if len(names) != len(series_as_tuple):
        raise ValueError("duplicate of series")

    for chunk in split_in_to_chunks(series_as_tuple, 200):
        requests: List["EntityRequest"] = [
            {"name": x[0], "ifModifiedSince": x[1].isoformat() if x[1] else None} for x in chunk
        ]
        response_list = self.session.series.post_fetch_series(*requests)
        for response, request in zip(response_list, requests):
            ret = _create_series(response, request["name"], self.session)
            if ret.status_code == StatusCode.NOT_MODIFIED and not include_not_modified:
                continue
            yield ret


def get_unified_series(
    self: "WebApi",
    *series_entries: Union[SeriesEntry, str],
    frequency: SeriesFrequency = SeriesFrequency.HIGHEST,
    weekdays: SeriesWeekdays = SeriesWeekdays.FULL_WEEK,
    calendar_merge_mode: CalendarMergeMode = CalendarMergeMode.AVAILABLE_IN_ANY,
    currency: str = "",
    start_point: Optional["StartOrEndPoint"] = None,
    end_point: Optional["StartOrEndPoint"] = None,
    raise_error: Optional[bool] = None
) -> UnifiedSeriesList:
    def convert_to_unified_series_entry(entry_or_name: Union[SeriesEntry, str]) -> "UnifiedSeriesEntry":
        if isinstance(entry_or_name, str):
            entry_or_name = SeriesEntry(entry_or_name)
        entrie = entry_or_name
        return {
            "name": entrie.name,
            "vintage": entrie.vintage.isoformat() if entrie.vintage is not None else None,
            "missingValueMethod": entrie.missing_value_method,
            "partialPeriodsMethod": entrie.partial_periods_method,
            "toLowerFrequencyMethod": entrie.to_lower_frequency_method,
            "toHigherFrequencyMethod": entrie.to_higher_frequency_method,
        }

    web_series_entries = [convert_to_unified_series_entry(x) for x in series_entries]

    request: "UnifiedSeriesRequest" = {
        "frequency": frequency,
        "weekdays": weekdays,
        "calendarMergeMode": calendar_merge_mode,
        "currency": currency,
        "seriesEntries": web_series_entries,
    }

    if start_point:
        request["startPoint"] = start_point.time
        request["startDateMode"] = start_point.mode

    if end_point:
        request["endPoint"] = end_point.time
        request["endDateMode"] = end_point.mode

    response = self.session.series.fetch_unified_series(request)

    str_dates = response.get("dates")

    dates = [_parse_iso8601(x) for x in str_dates] if str_dates else []

    series: List[UnifiedSeries] = []
    for i, one_series in enumerate(response["series"]):
        name = request["seriesEntries"][i]["name"]
        error_text = one_series.get("errorText")

        if error_text:
            series.append(UnifiedSeries(name, error_text, {}, []))
        else:
            values = [float(x) if x is not None else x for x in cast(List[Optional[float]], one_series["values"])]

            metadata = self.session._create_metadata(one_series["metadata"])

            series.append(UnifiedSeries(name, "", metadata, values))

    ret = UnifiedSeriesList(series, dates)

    if self.raise_error if raise_error is None else raise_error:
        errors = [EntityErrorInfo(x, y) for x, y in ret.get_errors().items()]
        if errors:
            raise GetEntitiesError(errors)

    return ret
