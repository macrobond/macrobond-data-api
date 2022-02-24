# -*- coding: utf-8 -*-

# pylint: disable = multiple-statements

from typing import Tuple, Union, TYPE_CHECKING
from abc import ABC, abstractmethod

from ._return_data_frame import _ReturnDataFrame

if TYPE_CHECKING:  # pragma: no cover

    from .enums import SeriesMissingValueMethod, SeriesToLowerFrequencyMethod, \
        SeriesToHigherFrequencyMethod, SeriesPartialPeriodsMethod, SeriesFrequency, \
        SeriesWeekdays, CalendarMergeMode

    from .entity import Entity, EntityColumns, EntityTypedDict
    from .series import Series, SeriesColumns, SeriesTypedDict
    from .unified_series import UnifiedSeries, UnifiedSeriesColumns, UnifiedSeriesTypedDict
    from .start_or_end_point import StartOrEndPoint


class GetOneSeriesReturn(_ReturnDataFrame, ABC):

    @abstractmethod
    def object(self) -> 'Series': ...

    @abstractmethod
    def dict(self) -> 'SeriesTypedDict': ...


class GetSeriesReturn(_ReturnDataFrame, ABC):

    @abstractmethod
    def tuple_of_objects(self) -> Tuple['Series', ...]: ...

    @abstractmethod
    def tuple_of_dicts(self) -> Tuple['SeriesTypedDict', ...]: ...


class GetOneEntitieReturn(_ReturnDataFrame, ABC):

    @abstractmethod
    def object(self) -> 'Entity': ...

    @abstractmethod
    def dict(self) -> 'EntityTypedDict': ...


class GetEntitiesReturn(_ReturnDataFrame, ABC):

    @abstractmethod
    def tuple_of_objects(self) -> Tuple['Entity', ...]: ...

    @abstractmethod
    def tuple_of_dicts(self) -> Tuple['EntityTypedDict', ...]: ...


class GetUnifiedSeriesReturn(_ReturnDataFrame, ABC):

    @abstractmethod
    def object(self) -> 'UnifiedSeries': ...

    @abstractmethod
    def dict(self) -> 'UnifiedSeriesTypedDict': ...


class SeriesMethods(ABC):

    @abstractmethod
    def get_one_series(self, series_name: str) -> GetOneSeriesReturn:
        '''Download one series.'''

    @abstractmethod
    def get_series(self, *series_names: str) -> GetSeriesReturn:
        '''Download one or more series.'''

    @abstractmethod
    def get_one_entitie(self, entity_name: str) -> GetOneEntitieReturn:
        '''Download one entity.'''

    @abstractmethod
    def get_entities(self, *entity_names: str) -> GetEntitiesReturn:
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
    ) -> GetUnifiedSeriesReturn:
        ...  # pragma: no cover


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
