# -*- coding: utf-8 -*-

from typing import Optional, Tuple, Any, Union, Dict, List, TYPE_CHECKING

from datetime import datetime

from macrobond_financial.common import Entity, UnifiedSeries, UnifiedSerie, Series
import macrobond_financial.common.series_methods as SeriesMethods
from macrobond_financial.common.enums import SeriesWeekdays, SeriesFrequency

from macrobond_financial.common._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from .com_typs import Connection, Database, SeriesRequest, Series as ComSeries, \
        Entity as ComEntity
    from macrobond_financial.common import SeriesEntrie, StartOrEndPoint, CalendarMergeMode

    from macrobond_financial.common import SeriesEntrie, StartOrEndPoint

    from macrobond_financial.common.entity import EntityColumns, \
        EntityTypedDict, ErrorEntityTypedDict, EntityTypedDicts

    from macrobond_financial.common.series import SeriesColumns, \
        SeriesTypedDict, ErrorSeriesTypedDict, SeriesTypedDicts

    from macrobond_financial.common.unified_series import UnifiedSeriesColumns, \
        UnifiedSeriesTypedDict

    from macrobond_financial.common.entity import EntityColumns
    from macrobond_financial.common.series import SeriesColumns
    from macrobond_financial.common.unified_series import UnifiedSeriesColumns


def _fill_metadata_from_entity(com_entity: 'ComEntity', metadata: Union[dict, Any]) -> None:
    com_metadata = com_entity.Metadata
    for names_and_description in com_metadata.ListNames():
        meta_name = names_and_description[0]
        meta_values = com_metadata.GetValues(meta_name)
        if len(meta_values) == 1:
            metadata[meta_name] = meta_values[0]
        else:
            metadata[meta_name] = list(meta_values)

    if 'FullDescription' not in metadata:
        metadata['FullDescription'] = com_entity.Title


def _create_entity(com_entity: 'ComEntity', name: str) -> Entity:
    metadata: Dict[str, Any] = {'Name': name}

    if com_entity.IsError:
        return Entity(com_entity.ErrorMessage, metadata)

    _fill_metadata_from_entity(com_entity, metadata)

    return Entity('', metadata)


def _create_entity_dicts(com_entity: 'ComEntity', name: str) -> 'EntityTypedDicts':

    if com_entity.IsError:
        error_entity: 'ErrorEntityTypedDict' = {
            'Name': name,
            'ErrorMessage': com_entity.ErrorMessage
        }
        return error_entity

    metadata: 'EntityTypedDict' = {'Name': name}  # type: ignore

    _fill_metadata_from_entity(com_entity, metadata)

    return metadata


def _create_series(com_series: 'ComSeries', name: str) -> Series:
    metadata: Dict[str, Any] = {'Name': name}

    if com_series.IsError:
        return Series(com_series.ErrorMessage, metadata, None, None)

    _fill_metadata_from_entity(com_series, metadata)

    return Series('', metadata, com_series.Values, com_series.DatesAtStartOfPeriod)


def _create_series_dicts(com_series: 'ComSeries', name: str) -> 'SeriesTypedDicts':

    if com_series.IsError:
        error_series: 'ErrorSeriesTypedDict' = {
            'Name': name,
            'ErrorMessage': com_series.ErrorMessage
        }
        return error_series

    metadata: 'SeriesTypedDict' = {  # type: ignore
        'Name': name,
        'Values': com_series.Values,
        'Dates': com_series.DatesAtStartOfPeriod
    }

    _fill_metadata_from_entity(com_series, metadata)

    return metadata


class _GetOneSeriesReturn(SeriesMethods.GetOneSeriesReturn):

    def __init__(self, database: 'Database', series_name: str) -> None:
        self.__database = database
        self.__series_name = series_name

    def object(self) -> Series:
        com_series = self.__database.FetchOneSeries(self.__series_name)
        return _create_series(com_series, self.__series_name)

    def dict(self) -> 'SeriesTypedDicts':
        com_series = self.__database.FetchOneSeries(self.__series_name)
        return _create_series_dicts(com_series, self.__series_name)

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        pandas = _get_pandas()
        args = args[1:]
        kwargs['data'] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def values_and_dates_as_data_frame(self, *args, **kwargs) -> 'DataFrame':
        pandas = _get_pandas()
        com_series = self.__database.FetchOneSeries(self.__series_name)

        if com_series.IsError:
            error_series: 'ErrorSeriesTypedDict' = {
                'Name': self.__series_name,
                'ErrorMessage': com_series.ErrorMessage
            }
            kwargs['data'] = error_series

            return error_series
        else:
            series: 'SeriesTypedDict' = {  # type: ignore
                'Values': com_series.Values,
                'Dates': com_series.DatesAtStartOfPeriod
            }

            kwargs['data'] = series

        args = args[1:]
        return pandas.DataFrame(*args, **kwargs)


class _GetSeriesReturn(SeriesMethods.GetSeriesReturn):

    def __init__(self, database: 'Database', series_names: Tuple[str, ...]) -> None:
        self.__database = database
        self.__series_names = series_names

    def tuple_of_objects(self) -> Tuple[Series, ...]:
        com_series = self.__database.FetchSeries(self.__series_names)

        ret: List[Series] = []
        for i, com_one_series in enumerate(com_series):
            ret.append(_create_series(com_one_series, self.__series_names[i]))
        return tuple(ret)

    def tuple_of_dicts(self) -> Tuple['SeriesTypedDicts', ...]:
        com_series = self.__database.FetchSeries(self.__series_names)

        ret: List['SeriesTypedDicts'] = []
        for i, com_one_series in enumerate(com_series):
            ret.append(_create_series_dicts(com_one_series, self.__series_names[i]))
        return tuple(ret)

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        pandas = _get_pandas()
        args = args[1:]
        kwargs['data'] = self.tuple_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetOneEntitieReturn(SeriesMethods.GetOneEntitieReturn):

    def __init__(self, database: 'Database', entity_name: str) -> None:
        self.__database = database
        self.__entity_name = entity_name

    def object(self) -> Entity:
        com_entity = self.__database.FetchOneEntity(self.__entity_name)
        return _create_entity(com_entity, self.__entity_name)

    def dict(self) -> 'EntityTypedDicts':
        com_entity = self.__database.FetchOneEntity(self.__entity_name)
        return _create_entity_dicts(com_entity, self.__entity_name)

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        pandas = _get_pandas()
        args = args[1:]
        kwargs['data'] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def metadata_as_data_frame(self) -> 'DataFrame':
        pandas = _get_pandas()

        return pandas.DataFrame.from_dict(
            self.dict(), orient='index', columns=['Attributes']
        )


class _GetEntitiesReturn(SeriesMethods.GetEntitiesReturn):

    def __init__(self, database: 'Database', entity_names: Tuple[str, ...]) -> None:
        self.__database = database
        self.__entity_names = entity_names

    def tuple_of_objects(self) -> Tuple[Entity, ...]:
        com_entitys = self.__database.FetchEntities(self.__entity_names)

        ret: List[Entity] = []
        for i, com_one_entity in enumerate(com_entitys):
            ret.append(_create_entity(com_one_entity, self.__entity_names[i]))
        return tuple(ret)

    def tuple_of_dicts(self) -> Tuple['EntityTypedDicts', ...]:
        com_entitys = self.__database.FetchEntities(self.__entity_names)

        ret: List['EntityTypedDicts'] = []
        for i, com_one_entity in enumerate(com_entitys):
            ret.append(_create_entity_dicts(com_one_entity, self.__entity_names[i]))
        return tuple(ret)

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        pandas = _get_pandas()
        args = args[1:]
        kwargs['data'] = self.tuple_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetUnifiedSeriesReturn(SeriesMethods.GetUnifiedSeriesReturn):

    def __init__(
        self,
        database: 'Database',
        request: 'SeriesRequest'
    ) -> None:
        super().__init__()
        self.__database = database
        self.__request = request

    def object(self) -> UnifiedSeries:
        com_series = self.__database.FetchSeries(self.__request)
        dates: Optional[Tuple[datetime, ...]] = None
        series: List[UnifiedSerie] = []
        for com_one_series in com_series:
            if com_one_series.IsError:
                series.append(UnifiedSerie(com_one_series.ErrorMessage, None, None))
            else:
                metadata: Dict[str, Any] = {}
                com_metadata = com_one_series.Metadata
                for names_and_description in com_metadata.ListNames():
                    name = names_and_description[0]
                    values = com_metadata.GetValues(name)
                    if len(values) == 1:
                        metadata[name] = values[0]
                    else:
                        metadata[name] = list(values)

                series.append(UnifiedSerie('', metadata, com_one_series.Values))

                if dates is None:
                    dates = com_one_series.DatesAtStartOfPeriod

        return UnifiedSeries(dates, tuple(series))

    def dict(self) -> 'UnifiedSeriesTypedDict':
        raise NotImplementedError()

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        raise NotImplementedError()
        # pandas = _get_pandas()
        # args = args[1:]
        # kwargs['data'] = self.list_of_dicts()
        # return pandas.DataFrame(*args, **kwargs)


class _ComSeriesMethods(SeriesMethods.SeriesMethods):

    def __init__(self, connection: 'Connection') -> None:
        super().__init__()
        self.__database = connection.Database

    def get_one_series(self, series_name: str) -> SeriesMethods.GetOneSeriesReturn:
        return _GetOneSeriesReturn(self.__database, series_name)

    def get_series(self, *series_names: str) -> SeriesMethods.GetSeriesReturn:
        return _GetSeriesReturn(self.__database, series_names)

    def get_one_entitie(self, entity_name: str) -> SeriesMethods.GetOneEntitieReturn:
        return _GetOneEntitieReturn(self.__database, entity_name)

    def get_entities(self, *entity_names: str) -> SeriesMethods.GetEntitiesReturn:
        return _GetEntitiesReturn(self.__database, entity_names)

    def get_unified_series(
        self,
        *series_entries: Union['SeriesEntrie', str],
        frequency: SeriesFrequency = None,
        weekdays: SeriesWeekdays = None,
        calendar_merge_mode: 'CalendarMergeMode' = None,
        currency: str = None,
        start_point: 'StartOrEndPoint' = None,
        end_point: 'StartOrEndPoint' = None,
    ) -> SeriesMethods.GetUnifiedSeriesReturn:
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

        return _GetUnifiedSeriesReturn(self.__database, request)
