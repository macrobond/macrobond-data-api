# -*- coding: utf-8 -*-

from typing import Tuple, Optional, Union, Any, Dict, TYPE_CHECKING
from abc import ABC, abstractmethod

from datetime import datetime

from .enums import CalendarDateMode

if TYPE_CHECKING:  # pragma: no cover
    from .enums import SeriesMissingValueMethod, SeriesToLowerFrequencyMethod, \
        SeriesToHigherFrequencyMethod, SeriesPartialPeriodsMethod, SeriesFrequency, \
        SeriesWeekdays, CalendarMergeMode


class SeriesMethods(ABC):

    @abstractmethod
    def get_one_series(self, series_name: str) -> 'Series':
        '''Download one series.'''

    @abstractmethod
    def get_series(self, *series_names: str) -> Tuple['Series', ...]:
        '''Download one or more series.'''

    @abstractmethod
    def get_one_entitie(self, entity_name: str) -> 'Entity':
        '''Download one entity.'''

    @abstractmethod
    def get_entities(self, *entity_names: str) -> Tuple['Entity', ...]:
        '''Download one or more entitys.'''

    @abstractmethod
    def get_unified_series(
        self,
        *series_entries: Union['SeriesEntrie', str],
        frequency: 'SeriesFrequency' = None,
        weekdays: 'SeriesWeekdays' = None,
        calendar_merge_mode: 'CalendarMergeMode' = None,
        currency: str = None,
        start_point: 'StartOrEndPoint' = None,
        end_point: 'StartOrEndPoint' = None,
    ) -> Tuple['UnifiedSeries', ...]:
        ...  # pragma: no cover


class Entity(ABC):
    '''Interface for a database Macrobond entity.'''

    @abstractmethod
    def __str__(self):
        ...  # pragma: no cover

    @abstractmethod
    def __repr__(self):
        ...  # pragma: no cover

    @property
    @abstractmethod
    def name(self) -> str:
        '''The name of the entity.'''

    @property
    @abstractmethod
    def primary_name(self) -> str:
        '''The primary name of the entity.'''

    @property
    @abstractmethod
    def is_error(self) -> bool:
        '''
        Is true if the request resulted in an error.
        The ErrorMessage property contains the error message.
        '''

    @property
    @abstractmethod
    def error_message(self) -> str:
        '''
        The error message if IsError is true.
        Otherwise it is empty.
        '''

    @property
    @abstractmethod
    def title(self) -> str:
        '''The title of the entity.'''

    @property
    @abstractmethod
    def entity_type(self) -> str:
        '''The type of the entity.'''

    @property
    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        '''The metadata for the entity.'''


class Series(Entity):
    '''Interface for a Macrobond time series.'''

    @property
    @abstractmethod
    def values(self) -> Tuple[Optional[float], ...]:
        '''The values of the series.'''

    @property
    @abstractmethod
    def dates(self) -> Tuple[datetime, ...]:
        '''The dates of the series.'''

    @property
    @abstractmethod
    def start_date(self) -> datetime:
        '''The start date.'''

    @property
    @abstractmethod
    def end_date(self) -> datetime:
        '''The end date.'''

    @property
    @abstractmethod
    def frequency(self) -> 'SeriesFrequency':
        '''The calendar frequency.'''

    @property
    @abstractmethod
    def weekdays(self) -> 'SeriesWeekdays':
        '''The days of the week used for daily series.'''

    @abstractmethod
    def get_value_at_date(self, date_time: datetime) -> float:
        '''Get the value at or preceding a specific date.'''

    @abstractmethod
    def get_index_at_date(self, date_time: datetime) -> int:
        '''Get the index in the value vector at the specified date. Zero based.'''


class UnifiedSeries(Entity):

    @property
    @abstractmethod
    def values(self) -> Tuple[Optional[float], ...]:
        '''The values of the series.'''


class StartOrEndPoint():

    def __init__(self, time: str, mode: Optional[CalendarDateMode]) -> None:
        self.time = time
        self.mode = CalendarDateMode.DATA_IN_ANY_SERIES if mode is None else mode

    def __str__(self):
        return self.time + ' mode:' + str(self.mode)

    def __repr__(self):
        return str(self)

    @staticmethod
    def relative_to_observations(
        observations: int, mode: CalendarDateMode = None
    ) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(observations), mode)

    @staticmethod
    def relative_to_years(years: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(years) + "y", mode)

    @staticmethod
    def relative_to_quarters(quarters: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(quarters) + "q", mode)

    @staticmethod
    def relative_to_months(months: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(months) + "m", mode)

    @staticmethod
    def relative_to_weeks(weeks: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(weeks) + "w", mode)

    @staticmethod
    def relative_to_days(days: int, mode: CalendarDateMode = None) -> 'StartOrEndPoint':
        return StartOrEndPoint(str(days) + "d", mode)

    @staticmethod
    def point_in_time(
        yyyy_or_datetime: Union[int, datetime],
        mm: Union[int, str] = None,  # pylint: disable = invalid-name
        dd: Union[int, str] = None  # pylint: disable = invalid-name
    ) -> 'StartOrEndPoint':
        if isinstance(yyyy_or_datetime, datetime):
            return StartOrEndPoint(yyyy_or_datetime.strftime('%Y-%m-%d'), None)
        time = str(yyyy_or_datetime).zfill(4)
        if mm is not None:
            time += '-' + str(mm).zfill(2)
            if dd is not None:
                time += '-' + str(dd).zfill(2)
        return StartOrEndPoint(time, None)

    @staticmethod
    def data_in_any_series() -> 'StartOrEndPoint':
        return StartOrEndPoint('', CalendarDateMode.DATA_IN_ANY_SERIES)

    @staticmethod
    def data_in_all_series() -> 'StartOrEndPoint':
        return StartOrEndPoint('', CalendarDateMode.DATA_IN_ALL_SERIES)


class SeriesEntrie():

    def __init__(
        self,
        name: str,
        missing_value_method: 'SeriesMissingValueMethod' = None,
        to_lowerfrequency_method: 'SeriesToLowerFrequencyMethod' = None,
        to_higherfrequency_method: 'SeriesToHigherFrequencyMethod' = None,
        partial_periods_method: 'SeriesPartialPeriodsMethod' = None,
    ) -> None:
        self.name = name
        self.missing_value_method = missing_value_method
        self.to_lowerfrequency_method = to_lowerfrequency_method
        self.to_higherfrequency_method = to_higherfrequency_method
        self.partial_periods_method = partial_periods_method
