# -*- coding: utf-8 -*-

# pylint: disable = multiple-statements

from typing import Tuple, Union, overload, List, TYPE_CHECKING
from abc import ABC, abstractmethod

from .enums import SeriesMissingValueMethod, SeriesToLowerFrequencyMethod, \
    SeriesToHigherFrequencyMethod, SeriesPartialPeriodsMethod

if TYPE_CHECKING:  # pragma: no cover

    from .enums import SeriesFrequency, SeriesWeekdays, CalendarMergeMode

    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

    from .entity import Entity, EntityColumns, EntityTypedDicts
    from .series import Series, SeriesColumns, SeriesTypedDicts
    from .unified_series import UnifiedSeries, UnifiedSeriesColumns, UnifiedSeriesTypedDict
    from .start_or_end_point import StartOrEndPoint

    from typing_extensions import Literal

    SeriesValuesAndDatesColumns = List[Literal['Values', 'Dates']]


class GetOneSeriesReturn(ABC):

    @abstractmethod
    def object(self) -> 'Series': ...

    @abstractmethod
    def dict(self) -> 'SeriesTypedDicts': ...

    @overload
    def data_frame(self) -> 'DataFrame': ...

    @overload
    def data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: Union[
            'SeriesColumns', 'pandas_typing.Axes'
        ] = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...

    @overload
    def values_and_dates_as_data_frame(self) -> 'DataFrame': ...

    @overload
    def values_and_dates_as_data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: Union[
            'SeriesValuesAndDatesColumns', 'pandas_typing.Axes'
        ] = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @abstractmethod
    def values_and_dates_as_data_frame(self, *args, **kwargs) -> 'DataFrame': ...


class GetSeriesReturn(ABC):

    @abstractmethod
    def tuple_of_objects(self) -> Tuple['Series', ...]: ...

    @abstractmethod
    def tuple_of_dicts(self) -> Tuple['SeriesTypedDicts', ...]: ...

    @overload
    def data_frame(self) -> 'DataFrame': ...

    @overload
    def data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: Union[
            'SeriesColumns', 'pandas_typing.Axes'
        ] = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...


class GetOneEntitieReturn(ABC):

    @abstractmethod
    def object(self) -> 'Entity': ...

    @abstractmethod
    def dict(self) -> 'EntityTypedDicts': ...

    @overload
    def data_frame(self) -> 'DataFrame': ...

    @overload
    def data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: Union[
            'EntityColumns', 'pandas_typing.Axes'
        ] = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...

    @abstractmethod
    def metadata_as_data_frame(self) -> 'DataFrame': ...

    # .from_dict(i['metadata'], orient='index')


class GetEntitiesReturn(ABC):

    @abstractmethod
    def tuple_of_objects(self) -> Tuple['Entity', ...]: ...

    @abstractmethod
    def tuple_of_dicts(self) -> Tuple['EntityTypedDicts', ...]: ...

    @overload
    def data_frame(self) -> 'DataFrame': ...

    @overload
    def data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: Union[
            'EntityColumns', 'pandas_typing.Axes'
        ] = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...


class GetUnifiedSeriesReturn(ABC):

    @abstractmethod
    def object(self) -> 'UnifiedSeries': ...

    @abstractmethod
    def dict(self) -> 'UnifiedSeriesTypedDict': ...

    @abstractmethod
    def data_frame(self, columns: List[str] = None) -> 'DataFrame': ...


class SeriesMethods(ABC):

    @abstractmethod
    def get_one_series(self, series_name: str, raise_get_entities_error=True) -> GetOneSeriesReturn:
        '''Download one series.'''

    @abstractmethod
    def get_series(self, *series_names: str, raise_get_entities_error=True) -> GetSeriesReturn:
        '''Download one or more series.'''

    @abstractmethod
    def get_one_entitie(
        self, entity_name: str, raise_get_entities_error=True
    ) -> GetOneEntitieReturn:
        '''Download one entity.'''

    @abstractmethod
    def get_entities(self, *entity_names: str, raise_get_entities_error=True) -> GetEntitiesReturn:
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
        raise_get_entities_error=True
    ) -> GetUnifiedSeriesReturn:
        ...  # pragma: no cover


class SeriesEntrie():

    def __init__(
        self,
        name: str,
        missing_value_method: SeriesMissingValueMethod = None,
        to_lowerfrequency_method: SeriesToLowerFrequencyMethod = None,
        to_higherfrequency_method: SeriesToHigherFrequencyMethod = None,
        partial_periods_method: SeriesPartialPeriodsMethod = None,
    ) -> None:
        self.name = name

        self.missing_value_method = \
            missing_value_method or SeriesMissingValueMethod.NONE

        self.to_lowerfrequency_method = \
            to_lowerfrequency_method or SeriesToLowerFrequencyMethod.AUTO

        self.to_higherfrequency_method = \
            to_higherfrequency_method or SeriesToHigherFrequencyMethod.AUTO

        self.partial_periods_method = \
            partial_periods_method or SeriesPartialPeriodsMethod.NONE
