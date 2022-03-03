# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from collections import OrderedDict
from typing import (
    Any,
    Dict,
    Sequence,
    Tuple,
    List,
    Optional,
    Union,
    cast,
    TYPE_CHECKING,
)

from datetime import datetime, timezone

from macrobond_financial.common import (
    Entity,
    UnifiedSeries,
    UnifiedSerie,
    Series,
    GetEntitiesError,
    EntitieErrorInfo,
)

from macrobond_financial.common.enums import (
    SeriesWeekdays,
    SeriesFrequency,
    CalendarMergeMode,
)

import macrobond_financial.common.series_methods as SeriesMethods

from macrobond_financial.common._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from .session import Session
    from pandas import DataFrame  # type: ignore
    from macrobond_financial.common import SeriesEntrie, StartOrEndPoint

    from macrobond_financial.common.entity import (
        EntityColumns,
        EntityTypedDict,
        ErrorEntityTypedDict,
        EntityTypedDicts,
    )

    from macrobond_financial.common.series import (
        SeriesColumns,
        SeriesTypedDict,
        ErrorSeriesTypedDict,
        SeriesTypedDicts,
    )

    from macrobond_financial.common.unified_series import (
        UnifiedSeriesColumns,
        UnifiedSeriesTypedDict,
    )

    from .web_typs.series_response import SeriesResponse
    from .web_typs.entity_response import EntityResponse
    from .web_typs.unified_series_request import (
        UnifiedSeriesRequest,
        UnifiedSeriesEntry,
    )
    from .web_typs.values_response import ValuesResponse


def _raise_get_entities_error(
    _raise: bool,
    response: Union[Sequence["EntityResponse"], Sequence["SeriesResponse"]],
    names: Sequence[str],
) -> None:
    if not _raise:
        return

    entities: List[EntitieErrorInfo] = []
    for i, entitie in enumerate(response):
        error_text = entitie.get("errorText")
        if error_text is not None:
            entities.append(EntitieErrorInfo(names[i], error_text))

    if len(entities) != 0:
        raise GetEntitiesError(entities)


def _create_entity(response: "EntityResponse", name: str) -> Entity:
    error_text = response.get("errorText")

    if error_text is not None:
        return Entity(error_text, {"Name": name})

    return Entity("", cast(Dict[str, Any], response["metadata"]))


def _create_entity_dicts(response: "EntityResponse", name: str) -> "EntityTypedDicts":
    error_text = response.get("errorText")

    if error_text is not None:
        error_entity: "ErrorEntityTypedDict" = {
            "Name": name,
            "ErrorMessage": error_text,
        }
        return error_entity

    return cast("EntityTypedDict", response["metadata"])


def _create_series(response: "SeriesResponse", name: str) -> Series:
    error_text = response.get("errorText")

    if error_text is not None:
        metadata: Dict[str, Any] = {"Name": name}
        return Series(error_text, metadata, None, None)

    dates = tuple(
        map(
            lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=timezone.utc
            ),
            cast(List[str], response["dates"]),
        )
    )

    values = cast(Tuple[Optional[float]], response["values"])
    return Series("", cast(Dict[str, Any], response["metadata"]), values, dates)


def _create_series_dicts(response: "SeriesResponse", name: str) -> "SeriesTypedDicts":
    error_text = response.get("errorText")

    if error_text is not None:
        error_series: "ErrorSeriesTypedDict" = {
            "Name": name,
            "ErrorMessage": error_text,
        }
        return error_series

    dates = tuple(
        map(
            lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=timezone.utc
            ),
            cast(List[str], response["dates"]),
        )
    )

    values = cast(Tuple[Optional[float]], response["values"])

    series: "SeriesTypedDict" = {  # type: ignore
        "Name": name,
        "Values": values,
        "Dates": dates,
    }

    return series


class _GetOneSeriesReturn(SeriesMethods.GetOneSeriesReturn):
    def __init__(self, session: "Session", series_name: str, _raise: bool) -> None:
        self.__session = session
        self.__series_name = series_name
        self.__raise = _raise

    def object(self) -> Series:
        response = self.__session.series.fetch_series(self.__series_name)

        _raise_get_entities_error(self.__raise, response, [self.__series_name])

        return _create_series(response[0], self.__series_name)

    def dict(self) -> "SeriesTypedDicts":
        response = self.__session.series.fetch_series(self.__series_name)

        _raise_get_entities_error(self.__raise, response, [self.__series_name])

        return _create_series_dicts(response[0], self.__series_name)

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        response = self.__session.series.fetch_series(self.__series_name)

        _raise_get_entities_error(self.__raise, response, [self.__series_name])

        response_entitie = response[0]
        error_text = response_entitie.get("errorText")

        if error_text is not None:
            error_series: "ErrorSeriesTypedDict" = {
                "Name": self.__series_name,
                "ErrorMessage": error_text,
            }
            kwargs["data"] = error_series
        else:

            dates = tuple(
                map(
                    lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                        tzinfo=timezone.utc
                    ),
                    cast(List[str], response_entitie["dates"]),
                )
            )

            values = cast(Tuple[Optional[float]], response_entitie["values"])

            series: "SeriesTypedDict" = {  # type: ignore
                "Values": values,
                "Dates": dates,
            }

            kwargs["data"] = series

        args = args[1:]
        return pandas.DataFrame(*args, **kwargs)


class _GetSeriesReturn(SeriesMethods.GetSeriesReturn):
    def __init__(
        self, session: "Session", series_names: Tuple[str, ...], _raise: bool
    ) -> None:
        self.__session = session
        self.__series_names = series_names
        self.__raise = _raise

    def tuple_of_objects(self) -> Tuple[Series, ...]:
        response = self.__session.series.fetch_series(*self.__series_names)

        _raise_get_entities_error(self.__raise, response, self.__series_names)

        return tuple(list(map(_create_series, response, self.__series_names)))

    def tuple_of_dicts(self) -> Tuple["SeriesTypedDicts", ...]:
        response = self.__session.series.fetch_series(*self.__series_names)

        _raise_get_entities_error(self.__raise, response, self.__series_names)

        return tuple(list(map(_create_series_dicts, response, self.__series_names)))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.tuple_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetOneEntitieReturn(SeriesMethods.GetOneEntitieReturn):
    def __init__(self, session: "Session", entity_name: str, _raise: bool) -> None:
        self.__session = session
        self.__entity_name = entity_name
        self.__raise = _raise

    def object(self) -> Entity:
        response = self.__session.series.fetch_entities(self.__entity_name)

        _raise_get_entities_error(self.__raise, response, [self.__entity_name])

        return _create_entity(response[0], self.__entity_name)

    def dict(self) -> "EntityTypedDicts":
        response = self.__session.series.fetch_entities(self.__entity_name)

        _raise_get_entities_error(self.__raise, response, [self.__entity_name])

        return _create_entity_dicts(response[0], self.__entity_name)

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def metadata_as_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()

        return pandas.DataFrame.from_dict(
            self.dict(), orient="index", columns=["Attributes"]
        )


class _GetEntitiesReturn(SeriesMethods.GetEntitiesReturn):
    def __init__(
        self, session: "Session", entity_names: Tuple[str, ...], _raise: bool
    ) -> None:
        self.__session = session
        self.__entity_names = entity_names
        self.__raise = _raise

    def tuple_of_objects(self) -> Tuple[Entity, ...]:
        response = self.__session.series.fetch_entities(*self.__entity_names)

        _raise_get_entities_error(self.__raise, response, self.__entity_names)

        return tuple(list(map(_create_entity, response, self.__entity_names)))

    def tuple_of_dicts(self) -> Tuple["EntityTypedDicts", ...]:
        response = self.__session.series.fetch_entities(*self.__entity_names)

        _raise_get_entities_error(self.__raise, response, self.__entity_names)

        return tuple(list(map(_create_entity_dicts, response, self.__entity_names)))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.tuple_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetUnifiedSeriesReturn(SeriesMethods.GetUnifiedSeriesReturn):
    def __init__(
        self, session: "Session", request: "UnifiedSeriesRequest", _raise: bool
    ) -> None:
        super().__init__()
        self.__session = session
        self.__request = request
        self.__raise = _raise

    def object(self) -> UnifiedSeries:
        response = self.__session.series.fetch_unified_series(self.__request)

        str_dates = response.get("dates")
        if str_dates is not None:
            dates = tuple(
                map(
                    lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                        tzinfo=timezone.utc
                    ),
                    cast(List[str], str_dates),
                )
            )
        else:
            dates = tuple()

        if self.__raise:
            entities: List[EntitieErrorInfo] = []
            for i, entitie in enumerate(response["series"]):
                error_text = entitie.get("errorText")
                if error_text is not None:
                    name = self.__request["seriesEntries"][i]["name"]
                    entities.append(EntitieErrorInfo(name, error_text))

            if len(entities) != 0:
                raise GetEntitiesError(entities)

        series: List[UnifiedSerie] = []
        for one_series in response["series"]:
            error_text = one_series.get("errorText")

            if error_text is not None:
                series.append(UnifiedSerie(error_text, None, None))
            else:
                values = cast(Tuple[Optional[float]], one_series["values"])
                series.append(UnifiedSerie("", one_series["metadata"], values))

        return UnifiedSeries(dates, tuple(series))

    def dict(self) -> "UnifiedSeriesTypedDict":
        raise NotImplementedError()

    def data_frame(self, columns: List[str] = None) -> "DataFrame":
        pandas = _get_pandas()
        response = self.__session.series.fetch_unified_series(self.__request)
        data: Dict[str, Any] = OrderedDict()

        dates_name = "dates" if not columns else columns[0]
        str_dates = response.get("dates")
        if str_dates is not None:
            data[dates_name] = tuple(
                map(
                    lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                        tzinfo=timezone.utc
                    ),
                    cast(List[str], str_dates),
                )
            )
        else:
            data[dates_name] = tuple()

        series_entries_names = list(
            map(lambda x: x["name"], self.__request["seriesEntries"])
        )

        for i, one_series in enumerate(response["series"]):
            error_text = one_series.get("errorText")

            if error_text is not None:
                ...
            else:
                values = cast(Tuple[Optional[float]], one_series["values"])
                name = series_entries_names[i] if not columns else columns[i + 1]
                data[name] = values

        return pandas.DataFrame.from_dict(data)


class _WebSeriesMethods(SeriesMethods.SeriesMethods):
    def __init__(self, session: "Session") -> None:
        super().__init__()
        self.__session = session

    def get_one_series(
        self, series_name: str, raise_get_entities_error=True
    ) -> SeriesMethods.GetOneSeriesReturn:
        return _GetOneSeriesReturn(
            self.__session, series_name, raise_get_entities_error
        )

    def get_series(
        self, *series_names: str, raise_get_entities_error=True
    ) -> SeriesMethods.GetSeriesReturn:
        return _GetSeriesReturn(self.__session, series_names, raise_get_entities_error)

    def get_one_entitie(
        self, entity_name: str, raise_get_entities_error=True
    ) -> SeriesMethods.GetOneEntitieReturn:
        return _GetOneEntitieReturn(
            self.__session, entity_name, raise_get_entities_error
        )

    def get_entities(
        self, *entity_names: str, raise_get_entities_error=True
    ) -> SeriesMethods.GetEntitiesReturn:
        return _GetEntitiesReturn(
            self.__session, entity_names, raise_get_entities_error
        )

    def get_unified_series(
        self,
        *series_entries: Union["SeriesEntrie", str],
        frequency: SeriesFrequency = None,
        weekdays: SeriesWeekdays = None,
        calendar_merge_mode: CalendarMergeMode = None,
        currency: str = None,
        start_point: "StartOrEndPoint" = None,
        end_point: "StartOrEndPoint" = None,
        raise_get_entities_error=True,
    ) -> SeriesMethods.GetUnifiedSeriesReturn:
        def convert_to_unified_series_entry(
            entrie_or_name: Union["SeriesEntrie", str]
        ) -> "UnifiedSeriesEntry":
            if isinstance(entrie_or_name, str):
                return cast("UnifiedSeriesEntry", {"name": entrie_or_name})
            return {
                "name": entrie_or_name.name,
                "missingValueMethod": entrie_or_name.missing_value_method,
                "partialPeriodsMethod": entrie_or_name.partial_periods_method,
                "toLowerFrequencyMethod": entrie_or_name.to_lowerfrequency_method,
                "toHigherFrequencyMethod": entrie_or_name.to_higherfrequency_method,
            }

        web_series_entries = list(map(convert_to_unified_series_entry, series_entries))

        request: "UnifiedSeriesRequest" = {
            "frequency": frequency,
            "weekdays": weekdays,
            "calendarMergeMode": calendar_merge_mode,
            "currency": currency,
            "seriesEntries": web_series_entries,
        }

        if start_point is not None:
            request["startPoint"] = start_point.time
            request["startDateMode"] = start_point.mode

        if end_point is not None:
            request["endPoint"] = end_point.time
            request["endDateMode"] = end_point.mode

        return _GetUnifiedSeriesReturn(
            self.__session, request, raise_get_entities_error
        )
