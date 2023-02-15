from math import isnan
from typing import List, Optional, Union, TYPE_CHECKING, Sequence

from datetime import datetime


from macrobond_data_api.common.enums import SeriesWeekdays, SeriesFrequency, CalendarMergeMode

from macrobond_data_api.common.types import (
    SeriesEntry,
    GetEntitiesError,
    Series,
    Entity,
    UnifiedSeriesList,
    UnifiedSeries,
)

from macrobond_data_api.common.types._repr_html_sequence import _ReprHtmlSequence

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from macrobond_data_api.common.types import StartOrEndPoint

    from .com_types import Series as ComSeries, Entity as ComEntity


def _datetime_to_datetime(dates: Sequence[datetime]) -> List[datetime]:
    return [datetime(x.year, x.month, x.day, x.hour, x.minute, x.second, x.microsecond) for x in dates]


def _create_entity(com_entity: "ComEntity", name: str) -> Entity:
    if com_entity.IsError:
        return Entity(name, com_entity.ErrorMessage, None)
    return Entity(name, None, _fill_metadata_from_entity(com_entity))


def _create_series(com_series: "ComSeries", name: str) -> Series:
    if com_series.IsError:
        return Series(name, com_series.ErrorMessage, None, None, None)
    return Series(
        name,
        None,
        _fill_metadata_from_entity(com_series),
        com_series.Values,
        _datetime_to_datetime(com_series.DatesAtStartOfPeriod),
    )


def get_one_series(self: "ComApi", series_name: str, raise_error: bool = None) -> Series:
    return self.get_series(series_name, raise_error=raise_error)[0]


def get_series(self: "ComApi", *series_names: str, raise_error: Optional[bool] = None) -> Sequence[Series]:
    com_series = self.database.FetchSeries(series_names)
    series = [_create_series(x, y) for x, y in zip(com_series, series_names)]
    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.error_message if y.is_error else None), series_names, series),
    )
    return _ReprHtmlSequence(series)


def get_one_entity(self: "ComApi", entity_name: str, raise_error: bool = None) -> Entity:
    return self.get_entities(entity_name, raise_error=raise_error)[0]


def get_entities(self: "ComApi", *entity_names: str, raise_error: bool = None) -> Sequence[Entity]:
    com_entitys = self.database.FetchEntities(entity_names)
    entitys = [_create_entity(x, y) for x, y in zip(com_entitys, entity_names)]
    GetEntitiesError._raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(lambda x, y: (x, y.error_message if y.is_error else None), entity_names, entitys),
    )
    return _ReprHtmlSequence(entitys)


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
            _fill_metadata_from_entity(com_one_series),
            [None if x is not None and isnan(x) else x for x in com_one_series.Values],
        )

    ret = UnifiedSeriesList([to_obj(request.AddedSeries[x].Name, y) for x, y in enumerate(com_series)], dates)

    errors = ret.get_errors()
    raise_error = self.raise_error if raise_error is None else raise_error
    if raise_error and len(errors) != 0:
        raise GetEntitiesError(errors)

    return ret
