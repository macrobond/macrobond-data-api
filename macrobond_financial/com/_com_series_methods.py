# -*- coding: utf-8 -*-

from typing import Tuple, Any, Union, Optional, Dict, TYPE_CHECKING, cast

from datetime import datetime

from macrobond_financial.common import SeriesMethods, \
    Entity as CommonEntity, \
    UnifiedSeries as CommonUnifiedSeries, \
    Series as CommonSeries

from macrobond_financial.common.enums import SeriesWeekdays, SeriesFrequency

if TYPE_CHECKING:  # pragma: no cover
    from .com_typs import Connection, Entity as ComEntity, Series as ComSeries
    from macrobond_financial.common import SeriesEntrie, StartOrEndPoint, CalendarMergeMode


class _Entity(CommonEntity):

    _com_type: 'ComEntity'
    _metadata: Dict[str, Any]

    def __init__(self, com_type: 'ComEntity') -> None:
        super().__init__()
        self._com_type = com_type

        if not self._com_type.IsError:
            metadata = {}
            com_metadata = com_type.Metadata
            for names_and_description in com_metadata.ListNames():
                name = names_and_description[0]
                values = com_metadata.GetValues(name)
                if len(values) == 1:
                    metadata[name] = values[0]
                else:
                    metadata[name] = list(values)
            self._metadata = metadata
        else:
            self._metadata = {}

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    @property
    def name(self) -> str:
        return self._com_type.Name

    @property
    def primary_name(self) -> str:
        return self._com_type.PrimaryName

    @property
    def is_error(self) -> bool:
        return self._com_type.IsError

    @property
    def error_message(self) -> str:
        return self._com_type.ErrorMessage

    @property
    def title(self) -> str:
        return self._com_type.Title

    @property
    def entity_type(self) -> str:
        return cast(str, self.metadata['EntityType'])

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata


class _UnifiedSeries(_Entity, CommonUnifiedSeries):

    _com_type: 'ComSeries'

    def __init__(self, com_type: 'ComSeries') -> None:
        super().__init__(com_type)

    @property
    def values(self) -> Tuple[Optional[float], ...]:
        return self._com_type.Values


class _Series(_Entity, CommonSeries):

    _com_type: 'ComSeries'

    def __init__(self, com_type: 'ComSeries') -> None:
        super().__init__(com_type)

    @property
    def values(self) -> Tuple[Optional[float], ...]:
        return self._com_type.Values

    @property
    def dates(self) -> Tuple[datetime, ...]:
        return self._com_type.DatesAtStartOfPeriod

    # @property
    # def forecast_flags(self) -> List[bool]:
    #     '''A vector with a flag for each value indicating if this is a forecast or not.'''
    #     return self._com_type.ForecastFlags

    @property
    def start_date(self) -> datetime:
        return self._com_type.StartDate

    @property
    def end_date(self) -> datetime:
        return self._com_type.EndDate

    @property
    def frequency(self) -> SeriesFrequency:
        return SeriesFrequency(self._com_type.Frequency)

    @property
    def weekdays(self) -> SeriesWeekdays:
        return SeriesWeekdays(self._com_type.Weekdays)

    def get_value_at_date(self, date_time: datetime) -> float:
        return self._com_type.GetValueAtDate(date_time)

    def get_index_at_date(self, date_time: datetime) -> int:
        return self._com_type.GetIndexAtDate(date_time)


class _ComSeriesMethods(SeriesMethods):

    def __init__(self, connection: 'Connection') -> None:
        super().__init__()
        self.__database = connection.Database

    def get_one_series(self, series_name: str) -> _Series:
        return _Series(self.__database.FetchOneSeries(series_name))

    def get_series(self, *series_names: str) -> Tuple[_Series, ...]:
        return tuple(map(_Series, self.__database.FetchSeries(series_names)))

    def get_one_entitie(self, entity_name: str) -> _Entity:
        return _Entity(self.__database.FetchOneEntity(entity_name))

    def get_entities(self, *entity_names: str) -> Tuple[_Entity, ...]:
        return tuple(map(_Entity, self.__database.FetchEntities(entity_names)))

    def get_unified_series(
        self,
        *series_entries: Union['SeriesEntrie', str],
        frequency: SeriesFrequency = None,
        weekdays: SeriesWeekdays = None,
        calendar_merge_mode: 'CalendarMergeMode' = None,
        currency: str = None,
        start_point: 'StartOrEndPoint' = None,
        end_point: 'StartOrEndPoint' = None,
    ) -> Tuple[_UnifiedSeries, ...]:
        request = self.__database.CreateUnifiedSeriesRequest()
        for entrie_or_name in series_entries:
            if isinstance(entrie_or_name, str):
                request.AddSeries(entrie_or_name)
                continue

            series_expression = request.AddSeries(entrie_or_name.name)

            if entrie_or_name.missing_value_method is not None:
                series_expression.MissingValueMethod = entrie_or_name.missing_value_method

            if entrie_or_name.to_lowerfrequency_method is not None:
                series_expression.ToLowerFrequencyMethod = entrie_or_name.to_lowerfrequency_method

            if entrie_or_name.to_higherfrequency_method is not None:
                series_expression.ToHigherFrequencyMethod = entrie_or_name.to_higherfrequency_method

            if entrie_or_name.partial_periods_method is not None:
                series_expression.PartialPeriodsMethod = entrie_or_name.partial_periods_method

        if frequency is not None:
            request.Frequency = frequency

        if weekdays is not None:
            request.Weekdays = weekdays

        if calendar_merge_mode is not None:
            request.CalendarMergeMode = calendar_merge_mode

        if currency is not None:
            request.Currency = currency

        if start_point is not None:
            request.StartDate = start_point.time
            request.StartDateMode = start_point.mode

        if end_point is not None:
            request.EndDate = end_point.time
            request.EndDateMode = end_point.mode

        return tuple(map(_UnifiedSeries, self.__database.FetchSeries(request)))
