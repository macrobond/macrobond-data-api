# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Tuple, List, Optional, Union, Any, cast, Dict, TYPE_CHECKING

from datetime import datetime, timezone

from macrobond_financial.common import SeriesMethods, \
    Metadata as CommonMetadata, \
    Entity as CommonEntity, \
    UnifiedSeries as CommonUnifiedSeries, \
    Series as CommonSeries

from macrobond_financial.common.enums import SeriesWeekdays, SeriesFrequency, CalendarMergeMode

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session
    from macrobond_financial.common import SeriesEntrie, StartOrEndPoint
    from .web_typs.series_response import SeriesResponse
    from .web_typs.entity_response import EntityResponse
    from .web_typs.unified_series_request import UnifiedSeriesRequest, UnifiedSeriesEntry
    from .web_typs.values_response import ValuesResponse


class _Metadata(CommonMetadata):

    _data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        super().__init__()
        self._data = data

    def __getitem__(self, name: str):
        return self._data[name]

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return str(self)

    def get_first_value(self, name: str) -> Optional[object]:
        val = self._data.get(name)
        if val is None:
            return None
        return val[0] if isinstance(val, list) else val

    def get_values(self, name: str) -> Union[Tuple[Any], Tuple]:
        val = self._data.get(name)
        if val is None:
            return ()
        if isinstance(val, list):
            return tuple(val)
        return (val,)

    def get_dict(self) -> Dict[str, Any]:
        return dict(self._data)


class _Entity(CommonEntity):

    _metadata: Optional[_Metadata]
    _error_message: str
    _error_name: str

    def __init__(self, entity_response: 'EntityResponse', name: str) -> None:
        super().__init__()
        self._error_name = name

        error_text: Optional[str] = entity_response.get('errorText')

        if error_text is None:
            self._error_message = ''

            metadata = entity_response.get('metadata')
            if not isinstance(metadata, dict):
                raise Exception('no metadata in data')
            self._metadata = _Metadata(metadata)
        else:
            self._error_message = error_text
            self._metadata = None

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    @property
    def name(self) -> str:
        if self._metadata is None:
            return self._error_name
        return self._metadata['Name']

    @property
    def primary_name(self) -> str:
        if self._metadata is None:
            return ''
        return self._metadata['PrimName']

    @property
    def is_error(self) -> bool:
        return self._error_message != ''

    @property
    def error_message(self) -> str:
        return self._error_message

    @property
    def title(self) -> str:
        if self._metadata is None:
            raise Exception(self._error_message)
        return self._metadata['FullDescription']

    @property
    def entity_type(self) -> str:
        if self._metadata is None:
            raise Exception(self._error_message)
        return self._metadata['EntityType']

    @property
    def metadata(self) -> CommonMetadata:
        if self._metadata is None:
            raise Exception(self._error_message)
        return self._metadata


class _UnifiedSeries(_Entity, CommonUnifiedSeries):

    _values: Optional[Tuple[float, ...]]

    def __init__(self, values_response: 'ValuesResponse', name: str) -> None:
        super().__init__(values_response, name)
        if self._metadata is not None:
            values = values_response.get("values")
            if values is not None:
                self._values = tuple(values)

    @property
    def values(self) -> Tuple[Optional[float], ...]:
        if self._values is None:
            raise Exception()
        return self._values


class _Series(_Entity, CommonSeries):

    _values: Optional[Tuple[float, ...]]

    _str_dates: Optional[List[str]]
    _dates: Optional[Tuple[datetime, ...]] = None

    def __init__(self, series_response: 'SeriesResponse', name: str) -> None:
        super().__init__(series_response, name)
        if self._metadata is not None:
            values = series_response.get("values")
            if values is not None:
                self._values = tuple(values)
            self._str_dates = series_response['dates']

    @property
    def values(self) -> Tuple[Optional[float], ...]:
        if self._values is None:
            raise Exception(self._error_message)
        return self._values

    @property
    def dates(self) -> Tuple[datetime, ...]:
        if self._metadata is None:
            raise Exception(self._error_message)
        if self._dates is None:
            self._dates = tuple(
                map(lambda s:
                    datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=timezone.utc),
                    cast(List[str], self._str_dates)
                    )
            )
            self._str_dates = None
        return self._dates

    @property
    def start_date(self) -> datetime:
        return self.dates[0]

    @property
    def end_date(self) -> datetime:
        return self.dates[len(self.dates) - 1]

    @property
    def frequency(self) -> SeriesFrequency:
        if self._metadata is None:
            raise Exception(self._error_message)
        return SeriesFrequency[self._metadata['Frequency'].upper()]

    @property
    def weekdays(self) -> SeriesWeekdays:
        if self._metadata is None:
            raise Exception(self._error_message)
        return SeriesWeekdays(self._metadata['DayMask'])

    def get_value_at_date(self, date_time: datetime) -> float:
        return cast(Tuple[float, ...], self._values)[self.dates.index(date_time)]

    def get_index_at_date(self, date_time: datetime) -> int:
        return self.dates.index(date_time)


class _WebSeriesMethods(SeriesMethods):

    def __init__(self, session: 'Session') -> None:
        super().__init__()
        self.__session = session

    def get_one_series(self, series_name: str) -> _Series:
        return self.get_series(series_name)[0]

    def get_series(self, *series_names: str) -> Tuple[_Series, ...]:
        series_list = self.__session.series.fetch_series(*series_names)

        ret: list[_Series] = []
        for i, series in enumerate(series_list):
            ret.append(_Series(series, series_names[i]))

        return tuple(ret)

    def get_one_entitie(self, entity_name: str) -> _Entity:
        return self.get_entities(entity_name)[0]

    def get_entities(self, *entity_names: str) -> Tuple[_Entity, ...]:
        entities_list = self.__session.series.fetch_entities(*entity_names)

        ret: list[_Entity] = []
        for i, entitie in enumerate(entities_list):
            ret.append(_Entity(entitie, entity_names[i]))

        return tuple(ret)

    def get_unified_series(
        self,
        *series_entries: Union['SeriesEntrie', str],
        frequency: SeriesFrequency = None,
        weekdays: SeriesWeekdays = None,
        calendar_merge_mode: CalendarMergeMode = None,
        currency: str = None,
        start_point: 'StartOrEndPoint' = None,
        end_point: 'StartOrEndPoint' = None,
    ) -> Tuple[_UnifiedSeries, ...]:

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

        response = self.__session.series.fetch_unified_series(request)

        ret: list[_UnifiedSeries] = []
        for i, entrie in enumerate(web_series_entries):
            ret.append(_UnifiedSeries(response['series'][i], entrie['name']))
        return tuple(ret)
