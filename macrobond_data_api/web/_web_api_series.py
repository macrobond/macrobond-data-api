# -*- coding: utf-8 -*-

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union, cast

from dateutil import parser  # type: ignore

from macrobond_data_api.common.types import SeriesEntry

from macrobond_data_api.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarMergeMode,
)

from macrobond_data_api.common.types import (
    GetEntitiesError,
    Series,
    Entity,
    UnifiedSeries,
    UnifiedSeriesList,
)

from .session import Session

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi

    from macrobond_data_api.common.types import StartOrEndPoint

    from .web_types import (
        UnifiedSeriesRequest,
        UnifiedSeriesEntry,
    )

    from .web_types import SeriesResponse, EntityResponse


__pdoc__ = {
    "WebApi.__init__": False,
}


def _optional_str_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    return parser.parse(datetime_str) if datetime_str else None


def _optional_str_to_datetime_no_utc(datetime_str: str) -> Optional[datetime]:
    return parser.parse(datetime_str, ignoretz=True) if datetime_str else None


def _str_to_datetime_no_utc(datetime_str: str) -> datetime:
    return parser.parse(datetime_str, ignoretz=True)


def _create_entity(response: "EntityResponse", name: str, session: Session) -> Entity:
    error_text = response.get("errorText")

    if error_text:
        return Entity(name, error_text, None)

    metadata = session._create_metadata(  # pylint: disable=protected-access
        cast(Dict[str, Any], response["metadata"])
    )

    return Entity(name, None, cast(Dict[str, Any], metadata))


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
    return Series(name, "", metadata, values, dates)


def get_one_series(self: "WebApi", series_name: str, raise_error: bool = None) -> Series:
    return self.get_series(series_name, raise_error=raise_error)[0]


def get_series(self, *series_names: str, raise_error: bool = None) -> List[Series]:
    response = self.session.series.fetch_series(*series_names)
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


def get_one_entity(self: "WebApi", entity_name: str, raise_error: bool = None) -> Entity:
    return self.get_entities(entity_name, raise_error=raise_error)[0]


def get_entities(self: "WebApi", *entity_names: str, raise_error: bool = None) -> List[Entity]:
    response = self.session.series.fetch_entities(*entity_names)
    entitys = list(map(lambda x, y: _create_entity(x, y, self.session), response, entity_names))
    GetEntitiesError.raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(
            lambda x, y: (x, y.error_message if y.is_error else None),
            entity_names,
            entitys,
        ),
    )
    return entitys


def get_unified_series(
    self: "WebApi",
    *series_entries: Union[SeriesEntry, str],
    frequency=SeriesFrequency.HIGHEST,
    weekdays: SeriesWeekdays = SeriesWeekdays.FULL_WEEK,
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
    currency="",
    start_point: "StartOrEndPoint" = None,
    end_point: "StartOrEndPoint" = None,
    raise_error: bool = None
) -> UnifiedSeriesList:
    def convert_to_unified_series_entry(
        entry_or_name: Union[SeriesEntry, str]
    ) -> "UnifiedSeriesEntry":
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

    web_series_entries = list(map(convert_to_unified_series_entry, series_entries))

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
    if str_dates:
        dates = tuple(map(_str_to_datetime_no_utc, str_dates))
    else:
        dates = tuple()

    series: List[UnifiedSeries] = []
    for i, one_series in enumerate(response["series"]):
        name = request["seriesEntries"][i]["name"]
        error_text = one_series.get("errorText")

        if error_text:
            series.append(UnifiedSeries(name, error_text, {}, tuple()))
        else:
            values = tuple(
                map(
                    lambda x: float(x) if x else None,
                    cast(List[Optional[float]], one_series["values"]),
                )
            )

            metadata = self.session._create_metadata(  # pylint: disable=protected-access
                cast(Dict[str, Any], one_series["metadata"])
            )

            series.append(UnifiedSeries(name, "", metadata, values))

    ret = UnifiedSeriesList(series, dates)

    errors = ret.get_errors()
    raise_error = self.raise_error if raise_error is None else raise_error
    if raise_error and len(errors) != 0:
        raise GetEntitiesError(errors)

    return ret
