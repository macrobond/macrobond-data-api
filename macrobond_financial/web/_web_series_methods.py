# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Any, Dict, Tuple, List, Optional, Union, cast, TYPE_CHECKING

from datetime import datetime, timezone

from macrobond_financial.common import Entity, UnifiedSeries, UnifiedSerie, Series

from macrobond_financial.common.enums import SeriesWeekdays, SeriesFrequency, CalendarMergeMode

import macrobond_financial.common.series_methods as SeriesMethods

# from macrobond_financial.common._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session
    from pandas import DataFrame  # type: ignore
    from macrobond_financial.common import SeriesEntrie, StartOrEndPoint

    from macrobond_financial.common.entity import EntityColumns, EntityTypedDict
    from macrobond_financial.common.series import SeriesColumns, SeriesTypedDict
    from macrobond_financial.common.unified_series import UnifiedSeriesColumns, \
        UnifiedSeriesTypedDict

    from .web_typs.series_response import SeriesResponse
    from .web_typs.entity_response import EntityResponse
    from .web_typs.unified_series_request import UnifiedSeriesRequest, UnifiedSeriesEntry
    from .web_typs.values_response import ValuesResponse


class _GetOneSeriesReturn(SeriesMethods.GetOneSeriesReturn):

    def __init__(self, session: 'Session', series_name: str) -> None:
        super().__init__()
        self.__session = session
        self.__series_name = series_name

    def object(self) -> Series:
        response = self.__session.series.fetch_series(self.__series_name)[0]
        error_text = response.get('errorText')

        if error_text is not None:
            return Series(error_text, {'Name': self.__series_name}, None, None)

        dates = tuple(
            map(lambda s:
                datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc),
                cast(List[str], response['dates'])
                )
        )

        values = cast(Tuple[Optional[float]], response['values'])

        return Series('', cast(Dict[str, Any], response['metadata']), values, dates)

    def dict(self) -> 'SeriesTypedDict':
        raise NotImplementedError()

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        raise NotImplementedError()
        # pandas = _get_pandas()
        # args = args[1:]
        # kwargs['data'] = self.list_of_dicts()
        # return pandas.DataFrame(*args, **kwargs)


class _GetSeriesReturn(SeriesMethods.GetSeriesReturn):

    def __init__(self, session: 'Session', series_names: Tuple[str, ...]) -> None:
        super().__init__()
        self.__session = session
        self.__series_names = series_names

    def tuple_of_objects(self) -> Tuple[Series, ...]:
        response_list = self.__session.series.fetch_series(*self.__series_names)

        ret: List[Series] = []
        for i, response in enumerate(response_list):
            error_text = response.get('errorText')

            if error_text is not None:
                metadata: Dict[str, Any] = {'Name': self.__series_names[i]}
                ret.append(Series(error_text, metadata, None, None))
            else:
                dates = tuple(
                    map(lambda s:
                        datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc),
                        cast(List[str], response['dates'])
                        )
                )

                values = cast(Tuple[Optional[float]], response['values'])
                ret.append(Series('', cast(Dict[str, Any], response['metadata']), values, dates))

        return tuple(ret)

    def tuple_of_dicts(self) -> Tuple['SeriesTypedDict', ...]:
        raise NotImplementedError()

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        raise NotImplementedError()
        # pandas = _get_pandas()
        # args = args[1:]
        # kwargs['data'] = self.list_of_dicts()
        # return pandas.DataFrame(*args, **kwargs)


class _GetOneEntitieReturn(SeriesMethods.GetOneEntitieReturn):

    def __init__(self, session: 'Session', entity_name: str) -> None:
        super().__init__()
        self.__session = session
        self.__entity_name = entity_name

    def object(self) -> Entity:
        response = self.__session.series.fetch_entities(self.__entity_name)[0]
        error_text = response.get('errorText')

        if error_text is not None:
            return Entity(error_text, {'Name': self.__entity_name})

        return Entity('', cast(Dict[str, Any], response['metadata']))

    def dict(self) -> 'EntityTypedDict':
        raise NotImplementedError()

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        raise NotImplementedError()
        # pandas = _get_pandas()
        # args = args[1:]
        # kwargs['data'] = self.list_of_dicts()
        # return pandas.DataFrame(*args, **kwargs)


class _GetEntitiesReturn(SeriesMethods.GetEntitiesReturn):

    def __init__(self, session: 'Session', entity_names: Tuple[str, ...]) -> None:
        super().__init__()
        self.__session = session
        self.__entity_names = entity_names

    def tuple_of_objects(self) -> Tuple[Entity, ...]:
        response_list = self.__session.series.fetch_entities(*self.__entity_names)

        ret: List[Entity] = []
        for i, response in enumerate(response_list):
            error_text = response.get('errorText')

            if error_text is not None:
                ret.append(Entity(error_text, {'Name': self.__entity_names[i]}))
            else:
                ret.append(Entity('', cast(Dict[str, Any], response['metadata'])))

        return tuple(ret)

    def tuple_of_dicts(self) -> Tuple['EntityTypedDict', ...]:
        raise NotImplementedError()

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        raise NotImplementedError()
        # pandas = _get_pandas()
        # args = args[1:]
        # kwargs['data'] = self.list_of_dicts()
        # return pandas.DataFrame(*args, **kwargs)


class _GetUnifiedSeriesReturn(SeriesMethods.GetUnifiedSeriesReturn):

    def __init__(
        self,
        session: 'Session',
        request: 'UnifiedSeriesRequest'
    ) -> None:
        super().__init__()
        self.__session = session
        self.__request = request

    def object(self) -> UnifiedSeries:
        response = self.__session.series.fetch_unified_series(self.__request)

        str_dates = response.get('dates')
        if str_dates is not None:
            dates = tuple(
                map(
                    lambda s:
                        datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc),
                    cast(List[str], str_dates)
                )
            )
        else:
            dates = tuple()

        series: List[UnifiedSerie] = []
        for one_series in response['series']:
            error_text = one_series.get('errorText')

            if error_text is not None:
                series.append(UnifiedSerie(error_text, None, None))
            else:
                values = cast(Tuple[Optional[float]], one_series['values'])
                series.append(UnifiedSerie('', one_series['metadata'], values))

        return UnifiedSeries(dates, tuple(series))

    def dict(self) -> 'UnifiedSeriesTypedDict':
        raise NotImplementedError()

    def data_frame(self, *args, **kwargs) -> 'DataFrame':
        raise NotImplementedError()
        # pandas = _get_pandas()
        # args = args[1:]
        # kwargs['data'] = self.list_of_dicts()
        # return pandas.DataFrame(*args, **kwargs)


class _WebSeriesMethods(SeriesMethods.SeriesMethods):

    def __init__(self, session: 'Session') -> None:
        super().__init__()
        self.__session = session

    def get_one_series(self, series_name: str) -> SeriesMethods.GetOneSeriesReturn:
        return _GetOneSeriesReturn(self.__session, series_name)

    def get_series(self, *series_names: str) -> SeriesMethods.GetSeriesReturn:
        return _GetSeriesReturn(self.__session, series_names)

    def get_one_entitie(self, entity_name: str) -> SeriesMethods.GetOneEntitieReturn:
        return _GetOneEntitieReturn(self.__session, entity_name)

    def get_entities(self, *entity_names: str) -> SeriesMethods.GetEntitiesReturn:
        return _GetEntitiesReturn(self.__session, entity_names)

    def get_unified_series(
        self,
        *series_entries: Union['SeriesEntrie', str],
        frequency: SeriesFrequency = None,
        weekdays: SeriesWeekdays = None,
        calendar_merge_mode: CalendarMergeMode = None,
        currency: str = None,
        start_point: 'StartOrEndPoint' = None,
        end_point: 'StartOrEndPoint' = None,
    ) -> SeriesMethods.GetUnifiedSeriesReturn:

        def convert_to_unified_series_entry(
            entrie_or_name: Union['SeriesEntrie', str]
        ) -> 'UnifiedSeriesEntry':
            if isinstance(entrie_or_name, str):
                return cast('UnifiedSeriesEntry', {'name': entrie_or_name})
            return {
                'name': entrie_or_name.name,
                'missingValueMethod': entrie_or_name.missing_value_method,
                'partialPeriodsMethod': entrie_or_name.partial_periods_method,
                'toLowerFrequencyMethod': entrie_or_name.to_lowerfrequency_method,
                'toHigherFrequencyMethod': entrie_or_name.to_higherfrequency_method,
            }

        web_series_entries = list(map(convert_to_unified_series_entry, series_entries))

        request: 'UnifiedSeriesRequest' = {
            'frequency': frequency,
            'weekdays': weekdays,
            'calendarMergeMode': calendar_merge_mode,
            'currency': currency,
            'seriesEntries': web_series_entries
        }

        if start_point is not None:
            request['startPoint'] = start_point.time
            request['startDateMode'] = start_point.mode

        if end_point is not None:
            request['endPoint'] = end_point.time
            request['endDateMode'] = end_point.mode

        return _GetUnifiedSeriesReturn(self.__session, request)
