from math import isnan
from typing import Generator, List, Optional, Tuple, Union, TYPE_CHECKING, Sequence

from datetime import datetime


from macrobond_data_api.common.enums import SeriesWeekdays, SeriesFrequency, CalendarMergeMode, StatusCode

from macrobond_data_api.common.types import (
    SeriesEntry,
    GetEntitiesError,
    EntityErrorInfo,
    Series,
    Entity,
    UnifiedSeriesList,
    UnifiedSeries,
)
from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence

from ._error_message_to_status_code import _error_message_to_status_code

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from macrobond_data_api.common.types import StartOrEndPoint

    from .com_types import Series as ComSeries, Entity as ComEntity


def _datetime_to_datetime(dates: Sequence[datetime]) -> List[datetime]:
    return [datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond) for x in dates]


def _create_entity(com_entity: "ComEntity", name: str, api: "ComApi") -> Entity:
    if com_entity.IsError:
        return Entity(name, com_entity.ErrorMessage, _error_message_to_status_code(com_entity), None)
    return Entity(name, None, StatusCode.OK, api._fill_metadata_from_entity(com_entity))


def _create_series(com_series: "ComSeries", name: str, api: "ComApi") -> Series:
    if com_series.IsError:
        return Series(name, com_series.ErrorMessage, _error_message_to_status_code(com_series), None, None, None, None)
    return Series(
        name,
        None,
        StatusCode.OK,
        api._fill_metadata_from_entity(com_series),
        None,
        [None if isnan(x) else x for x in com_series.Values],
        _datetime_to_datetime(com_series.DatesAtStartOfPeriod),
    )


def get_one_series(self: "ComApi", series_name: str, raise_error: bool = None) -> Series:
    return self.get_series([series_name], raise_error=raise_error)[0]


def get_series(self: "ComApi", series_names: Sequence[str], raise_error: Optional[bool] = None) -> Sequence[Series]:
    series_names = tuple(series_names)
    com_series = self.database.FetchSeries(series_names)
    series = [_create_series(x, y, self) for x, y in zip(com_series, series_names)]
    if self.raise_error if raise_error is None else raise_error:
        GetEntitiesError._raise_if([(x, y.error_message) for x, y in zip(series_names, series)])
    return _ReprHtmlSequence(series)


def get_one_entity(self: "ComApi", entity_name: str, raise_error: bool = None) -> Entity:
    return self.get_entities([entity_name], raise_error=raise_error)[0]


def get_entities(self: "ComApi", entity_names: Sequence[str], raise_error: bool = None) -> Sequence[Entity]:
    entity_names = tuple(entity_names)
    com_entitys = self.database.FetchEntities(entity_names)
    entitys = [_create_entity(x, y, self) for x, y in zip(com_entitys, entity_names)]
    if self.raise_error if raise_error is None else raise_error:
        GetEntitiesError._raise_if([(x, y.error_message) for x, y in zip(entity_names, entitys)])
    return _ReprHtmlSequence(entitys)


def get_many_series(
    self: "ComApi", series: Sequence[Union[str, Tuple[str, Optional[datetime]]]], include_not_modified: bool = False
) -> Generator[Series, None, None]:
    if len(series) == 0:
        yield from ()

    series_as_tuple: List[Tuple[str, Optional[datetime]]] = [(x, None) if isinstance(x, str) else x for x in series]

    names = {x[0] for x in series_as_tuple}

    if len(names) != len(series_as_tuple):
        raise ValueError("duplicate of series")

    for serie, serie_info in zip(self.get_series([x[0] for x in series_as_tuple], raise_error=False), series_as_tuple):
        if serie.is_error:
            yield serie
            continue

        if serie_info[1]:
            last_modified_time = serie.metadata["LastModifiedTimeStamp"]
            if last_modified_time <= serie_info[1]:
                if include_not_modified:
                    yield Series(serie_info[0], "Not modified", StatusCode.NOT_MODIFIED, None, None, None, None)
                continue

        yield serie


def get_unified_series(
    self: "ComApi",
    *series_entries: Union[SeriesEntry, str],
    frequency: SeriesFrequency = SeriesFrequency.HIGHEST,
    weekdays: SeriesWeekdays = SeriesWeekdays.FULL_WEEK,
    calendar_merge_mode: CalendarMergeMode = CalendarMergeMode.AVAILABLE_IN_ANY,
    currency: str = "",
    start_point: Optional["StartOrEndPoint"] = None,
    end_point: Optional["StartOrEndPoint"] = None,
    raise_error: Optional[bool] = None
) -> UnifiedSeriesList:
    request = self.database.CreateUnifiedSeriesRequest()
    for entry_or_name in series_entries:
        if isinstance(entry_or_name, str):
            entry_or_name = SeriesEntry(entry_or_name)

        entry = entry_or_name
        series_expression = request.AddSeries(entry.name)

        if entry.vintage:
            series_expression.Vintage = entry.vintage

        series_expression.MissingValueMethod = entry.missing_value_method

        series_expression.ToLowerFrequencyMethod = entry.to_lower_frequency_method

        series_expression.ToHigherFrequencyMethod = entry_or_name.to_higher_frequency_method

        series_expression.PartialPeriodsMethod = entry_or_name.partial_periods_method

    request.Frequency = frequency

    request.Weekdays = weekdays

    request.CalendarMergeMode = calendar_merge_mode

    request.Currency = currency

    if start_point:
        request.StartDate = start_point.time
        request.StartDateMode = start_point.mode

    if end_point:
        request.EndDate = end_point.time
        request.EndDateMode = end_point.mode

    com_series = self.database.FetchSeries(request)

    first = next(filter(lambda x: not x.IsError, com_series), None)
    dates = _datetime_to_datetime(first.DatesAtStartOfPeriod) if first else []

    def to_obj(name: str, com_one_series: "ComSeries") -> UnifiedSeries:
        if com_one_series.IsError:
            return UnifiedSeries(name, com_one_series.ErrorMessage, {}, [])

        return UnifiedSeries(
            name,
            "",
            self._fill_metadata_from_entity(com_one_series),
            [None if isnan(x) else x for x in com_one_series.Values],
        )

    ret = UnifiedSeriesList([to_obj(request.AddedSeries[x].Name, y) for x, y in enumerate(com_series)], dates)

    if self.raise_error if raise_error is None else raise_error:
        errors = [EntityErrorInfo(x, y) for x, y in ret.get_errors().items()]
        if errors:
            raise GetEntitiesError(errors)

    return ret
