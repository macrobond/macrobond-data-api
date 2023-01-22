# -*- coding: utf-8 -*-

from math import isnan
from typing import Any, Dict, List, Tuple, Union, TYPE_CHECKING, Sequence

from datetime import datetime

from macrobond_data_api.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarMergeMode,
)

from macrobond_data_api.common.types import (
    SeriesEntry,
    GetEntitiesError,
    Series,
    Entity,
    UnifiedSeriesList,
    UnifiedSeries,
)

if TYPE_CHECKING:  # pragma: no cover
    from .com_api import ComApi

    from macrobond_data_api.common.types import StartOrEndPoint

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


def get_series(self, *series_names: str, raise_error: bool = None) -> List[Series]:
    com_series = self.database.FetchSeries(series_names)
    series = list(map(_create_series, com_series, series_names))
    GetEntitiesError.raise_if(
        self.raise_error if raise_error is None else raise_error,
        map(
            lambda x, y: (x, y.error_message if y.is_error else None),
            series_names,
            series,
        ),
    )
    return series


def get_one_entity(self: "ComApi", entity_name: str, raise_error: bool = None) -> Entity:
    return self.get_entities(entity_name, raise_error=raise_error)[0]


def get_entities(self: "ComApi", *entity_names: str, raise_error: bool = None) -> List[Entity]:
    com_entitys = self.database.FetchEntities(entity_names)
    entitys = list(map(_create_entity, com_entitys, entity_names))
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
    self: "ComApi",
    *series_entries: Union[SeriesEntry, str],
    frequency=SeriesFrequency.HIGHEST,
    weekdays: SeriesWeekdays = SeriesWeekdays.FULL_WEEK,
    calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
    currency="",
    start_point: "StartOrEndPoint" = None,
    end_point: "StartOrEndPoint" = None,
    raise_error: bool = None
) -> UnifiedSeriesList:
    # pylint: disable=too-many-branches
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
    if first:
        dates = _datetime_to_datetime(first.DatesAtStartOfPeriod)
    else:
        dates = tuple()

    series: List[UnifiedSeries] = []

    for i, com_one_series in enumerate(com_series):
        name = request.AddedSeries[i].Name
        if com_one_series.IsError:
            series.append(UnifiedSeries(name, com_one_series.ErrorMessage, {}, tuple()))
            continue

        metadata: Dict[str, Any] = {}
        com_metadata = com_one_series.Metadata
        for names_and_description in com_metadata.ListNames():
            metadata_name = names_and_description[0]
            values = com_metadata.GetValues(metadata_name)
            if len(values) == 1:
                metadata[metadata_name] = values[0]
            else:
                metadata[metadata_name] = list(values)

        series.append(
            UnifiedSeries(
                name,
                "",
                metadata,
                tuple(
                    map(
                        lambda x: None if x is not None and isnan(x) else x,
                        com_one_series.Values,
                    )
                ),
            )
        )

    ret = UnifiedSeriesList(series, dates)

    errors = ret.get_errors()
    raise_error = self.raise_error if raise_error is None else raise_error
    if raise_error and len(errors) != 0:
        raise GetEntitiesError(errors)

    return ret
    # pylint: enable=too-many-branches
