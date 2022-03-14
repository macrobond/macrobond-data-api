# -*- coding: utf-8 -*-

from typing import Union, overload, List, TYPE_CHECKING
from abc import ABC, abstractmethod

from .enums import (
    SeriesMissingValueMethod,
    SeriesToLowerFrequencyMethod,
    SeriesToHigherFrequencyMethod,
    SeriesPartialPeriodsMethod,
    SeriesFrequency,
    SeriesWeekdays,
    CalendarMergeMode,
)

if TYPE_CHECKING:  # pragma: no cover

    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

    from .entity import Entity, EntityColumns, EntityTypedDict
    from .series import Series, SeriesColumns, SeriesTypedDict
    from .unified_series import UnifiedSeries, UnifiedSeriesDict
    from .start_or_end_point import StartOrEndPoint

    from typing_extensions import Literal

    SeriesValuesAndDatesColumns = List[Literal["Values", "Dates"]]


class GetOneSeriesReturn(ABC):
    @abstractmethod
    def object(self) -> "Series":
        ...

    @abstractmethod
    def dict(self) -> "SeriesTypedDict":
        ...

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["SeriesColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...

    @overload
    def values_and_dates_as_data_frame(self) -> "DataFrame":
        ...

    @overload
    def values_and_dates_as_data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["SeriesValuesAndDatesColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        ...


class GetSeriesReturn(ABC):
    @abstractmethod
    def list_of_objects(self) -> List["Series"]:
        ...

    @abstractmethod
    def list_of_dicts(self) -> List["SeriesTypedDict"]:
        ...

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["SeriesColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...


class GetOneEntitieReturn(ABC):
    @abstractmethod
    def object(self) -> "Entity":
        ...

    @abstractmethod
    def dict(self) -> "EntityTypedDict":
        ...

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["EntityColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...

    @abstractmethod
    def metadata_as_data_frame(self) -> "DataFrame":
        ...

    # .from_dict(i['metadata'], orient='index')


class GetEntitiesReturn(ABC):
    @abstractmethod
    def list_of_objects(self) -> List["Entity"]:
        ...

    @abstractmethod
    def list_of_dicts(self) -> List["EntityTypedDict"]:
        ...

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["EntityColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...


class GetUnifiedSeriesReturn(ABC):
    @abstractmethod
    def object(self) -> "UnifiedSeries":
        ...

    @abstractmethod
    def dict(self) -> "UnifiedSeriesDict":
        ...

    @abstractmethod
    def data_frame(self, columns: List[str] = None) -> "DataFrame":
        ...


class SeriesMethods(ABC):
    @abstractmethod
    def get_one_series(
        self, series_name: str, raise_error: bool = None
    ) -> GetOneSeriesReturn:
        """Download one series."""

    @abstractmethod
    def get_series(
        self, *series_names: str, raise_error: bool = None
    ) -> GetSeriesReturn:
        """Download one or more series."""

    @abstractmethod
    def get_one_entitie(
        self, entity_name: str, raise_error: bool = None
    ) -> GetOneEntitieReturn:
        """Download one entity."""

    @abstractmethod
    def get_entities(
        self, *entity_names: str, raise_error: bool = None
    ) -> GetEntitiesReturn:
        """Download one or more entitys."""

    @abstractmethod
    def get_unified_series(
        self,
        *series_entries: Union["SeriesEntrie", str],
        frequency=SeriesFrequency.HIGHEST,
        weekdays=SeriesWeekdays.FULL_WEEK,
        calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
        currency="",
        start_point: "StartOrEndPoint" = None,
        end_point: "StartOrEndPoint" = None,
        raise_error: bool = None
    ) -> GetUnifiedSeriesReturn:
        ...  # pragma: no cover


class SeriesEntrie:
    def __init__(
        self,
        name: str,
        missing_value_method=SeriesMissingValueMethod.NONE,
        to_lowerfrequency_method=SeriesToLowerFrequencyMethod.AUTO,
        to_higherfrequency_method=SeriesToHigherFrequencyMethod.AUTO,
        partial_periods_method=SeriesPartialPeriodsMethod.NONE,
    ) -> None:
        self.name = name
        self.missing_value_method = missing_value_method
        self.to_lowerfrequency_method = to_lowerfrequency_method
        self.to_higherfrequency_method = to_higherfrequency_method
        self.partial_periods_method = partial_periods_method
