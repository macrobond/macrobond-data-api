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
    SeriesEntrie,
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
    from .web_api import WebApi
    from pandas import DataFrame  # type: ignore
    from macrobond_financial.common import StartOrEndPoint

    from macrobond_financial.common.entity import (
        EntityTypedDict,
    )

    from macrobond_financial.common.series import (
        SeriesTypedDict,
    )

    from macrobond_financial.common.unified_series import (
        UnifiedSeriesDict,
        UnifiedSerieDict,
    )

    from .web_typs.series_response import SeriesResponse
    from .web_typs.entity_response import EntityResponse
    from .web_typs.unified_series_request import (
        UnifiedSeriesRequest,
        UnifiedSeriesEntry,
    )
    from .web_typs.unified_series_response import (
        UnifiedSeriesResponse,
    )


def _create_entity(response: "EntityResponse", name: str) -> Entity:
    error_text = response.get("errorText")

    if error_text:
        return Entity(name, error_text, None)

    return Entity(name, None, cast(Dict[str, Any], response["metadata"]))


def _add_metadata(
    source: Dict[str, Any], destination: Dict[str, Any] = None
) -> Dict[str, Any]:
    if not destination:
        destination = {}

    for key in source.keys():
        destination["metadata." + key] = source[key]

    return destination


def _create_entity_dicts(response: "EntityResponse", name: str) -> "EntityTypedDict":
    error_text = response.get("errorText")

    if error_text:
        error_entity: "EntityTypedDict" = {
            "Name": name,
            "ErrorMessage": error_text,
        }
        return error_entity

    return _add_metadata(response["metadata"], {"Name": name})  # type: ignore


def _create_series(response: "SeriesResponse", name: str) -> Series:
    error_text = response.get("errorText")

    if error_text:
        return Series(name, error_text, None, None, None)

    dates = tuple(
        map(
            lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                tzinfo=timezone.utc
            ),
            cast(List[str], response["dates"]),
        )
    )

    values = cast(Tuple[Optional[float]], response["values"])
    return Series(name, "", cast(Dict[str, Any], response["metadata"]), values, dates)


def _create_series_dicts(response: "SeriesResponse", name: str) -> "SeriesTypedDict":
    error_text = response.get("errorText")

    if error_text:
        error_series: "SeriesTypedDict" = {
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

    return _add_metadata(response["metadata"], series)  # type: ignore


class _GetSeriesReturnBase:
    def __init__(
        self, session: "Session", series_names: Sequence[str], _raise: bool
    ) -> None:
        self._session = session
        self._series_names = series_names
        self._raise = _raise

    def fetch_series(self) -> List["SeriesResponse"]:
        response = self._session.series.fetch_series(*self._series_names)
        GetEntitiesError.raise_if(
            self._raise,
            map(lambda x, y: (x, y.get("errorText")), self._series_names, response),
        )
        return response


class _GetOneSeriesReturn(_GetSeriesReturnBase, SeriesMethods.GetOneSeriesReturn):
    def object(self) -> Series:
        return _create_series(self.fetch_series()[0], self._series_names[0])

    def dict(self) -> "SeriesTypedDict":
        return _create_series_dicts(self.fetch_series()[0], self._series_names[0])

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        response = self.fetch_series()[0]
        error_text = response.get("errorText")

        if error_text:
            error_series: "SeriesTypedDict" = {
                "Name": self._series_names[0],
                "ErrorMessage": error_text,
            }
            kwargs["data"] = [error_series]
        else:

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
                "Values": values,
                "Dates": dates,
            }

            kwargs["data"] = series

        args = args[1:]
        return pandas.DataFrame(*args, **kwargs)


class _GetSeriesReturn(_GetSeriesReturnBase, SeriesMethods.GetSeriesReturn):
    def list_of_objects(self) -> List[Series]:
        response = self.fetch_series()
        return list(map(_create_series, response, self._series_names))

    def list_of_dicts(self) -> List["SeriesTypedDict"]:
        response = self.fetch_series()
        return list(map(_create_series_dicts, response, self._series_names))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetEntitiesReturnBase:
    def __init__(
        self, session: "Session", entity_names: Sequence[str], _raise: bool
    ) -> None:
        self._session = session
        self._entity_names = entity_names
        self._raise = _raise

    def fetch_entities(self) -> List["EntityResponse"]:
        response = self._session.series.fetch_entities(*self._entity_names)
        GetEntitiesError.raise_if(
            self._raise,
            map(lambda x, y: (x, y.get("errorText")), self._entity_names, response),
        )
        return response


class _GetOneEntitieReturn(_GetEntitiesReturnBase, SeriesMethods.GetOneEntitieReturn):
    def object(self) -> Entity:
        return _create_entity(self.fetch_entities()[0], self._entity_names[0])

    def dict(self) -> "EntityTypedDict":
        return _create_entity_dicts(self.fetch_entities()[0], self._entity_names[0])

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def metadata_as_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()

        entitie = self.fetch_entities()[0]

        error_text = entitie.get("errorText")
        if error_text:
            return pandas.DataFrame.from_dict(
                {
                    "Name": self._entity_names[0],
                    "ErrorMessage": error_text,
                },
                orient="index",
                columns=["Attributes"],
            )

        metadata = entitie["metadata"]

        return pandas.DataFrame.from_dict(
            metadata, orient="index", columns=["Attributes"]
        )


class _GetEntitiesReturn(_GetEntitiesReturnBase, SeriesMethods.GetEntitiesReturn):
    def list_of_objects(self) -> List[Entity]:
        response = self.fetch_entities()
        return list(map(_create_entity, response, self._entity_names))

    def list_of_dicts(self) -> List["EntityTypedDict"]:
        response = self.fetch_entities()
        return list(map(_create_entity_dicts, response, self._entity_names))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetUnifiedSeriesReturn(SeriesMethods.GetUnifiedSeriesReturn):
    def __init__(
        self, session: "Session", request: "UnifiedSeriesRequest", _raise: bool
    ) -> None:
        super().__init__()
        self._session = session
        self._request = request
        self._raise = _raise

    def fetch_unified_series(self) -> "UnifiedSeriesResponse":
        response = self._session.series.fetch_unified_series(self._request)

        GetEntitiesError.raise_if(
            self._raise,
            map(
                lambda x, y: (x["name"], y.get("errorText")),
                self._request["seriesEntries"],
                response["series"],
            ),
        )
        return response

    @classmethod
    def get_dates(cls, response: "UnifiedSeriesResponse") -> Tuple[datetime, ...]:
        str_dates = response.get("dates")
        if str_dates:
            return tuple(
                map(
                    lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                        tzinfo=timezone.utc
                    ),
                    cast(List[str], str_dates),
                )
            )
        return tuple()

    def object(self) -> UnifiedSeries:
        response = self.fetch_unified_series()

        dates = self.get_dates(response)

        series: List[UnifiedSerie] = []
        for i, one_series in enumerate(response["series"]):
            name = self._request["seriesEntries"][i]["name"]
            error_text = one_series.get("errorText")

            if error_text:
                series.append(UnifiedSerie(name, error_text, {}, tuple()))
            else:
                values = cast(Tuple[Optional[float]], one_series["values"])
                metadata = cast(Dict[str, Any], one_series["metadata"])
                series.append(UnifiedSerie(name, "", metadata, values))

        return UnifiedSeries(dates, tuple(series))

    def dict(self) -> "UnifiedSeriesDict":
        response = self.fetch_unified_series()
        dates = self.get_dates(response)
        series: List["UnifiedSerieDict"] = []
        for i, one_series in enumerate(response["series"]):
            name = self._request["seriesEntries"][i]["name"]
            error_text = one_series.get("errorText")
            if error_text:
                series.append(
                    {
                        "error_message": error_text,
                        "name": name,
                        "metadata": {},
                        "values": tuple(),
                    }
                )
            else:
                values = cast(Tuple[Optional[float]], one_series["values"])
                metadata = cast(Dict[str, Any], one_series["metadata"])
                series.append(
                    {
                        "error_message": "",
                        "name": name,
                        "values": values,
                        "metadata": metadata,
                    }
                )
        return {"dates": dates, "series": tuple(series)}

    def data_frame(self, columns: List[str] = None) -> "DataFrame":
        pandas = _get_pandas()
        response = self.fetch_unified_series()
        data: Dict[str, Any] = OrderedDict()

        dates_name = "dates" if not columns else columns[0]
        data[dates_name] = self.get_dates(response)

        for i, one_series in enumerate(response["series"]):
            if not one_series.get("errorText"):
                name = (
                    columns[i + 1]
                    if columns
                    else self._request["seriesEntries"][i]["name"]
                )
                data[name] = cast(Tuple[Optional[float]], one_series["values"])

        return pandas.DataFrame.from_dict(data)


class _WebSeriesMethods(SeriesMethods.SeriesMethods):
    def __init__(self, api: "WebApi") -> None:
        super().__init__()
        self.__api = api

    def get_one_series(
        self, series_name: str, raise_error: bool = None
    ) -> SeriesMethods.GetOneSeriesReturn:
        return _GetOneSeriesReturn(
            self.__api.session,
            [series_name],
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_series(
        self, *series_names: str, raise_error: bool = None
    ) -> SeriesMethods.GetSeriesReturn:
        return _GetSeriesReturn(
            self.__api.session,
            series_names,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_one_entitie(
        self, entity_name: str, raise_error: bool = None
    ) -> SeriesMethods.GetOneEntitieReturn:
        return _GetOneEntitieReturn(
            self.__api.session,
            [entity_name],
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_entities(
        self, *entity_names: str, raise_error: bool = None
    ) -> SeriesMethods.GetEntitiesReturn:
        return _GetEntitiesReturn(
            self.__api.session,
            entity_names,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_unified_series(
        self,
        *series_entries: Union[SeriesEntrie, str],
        frequency=SeriesFrequency.HIGHEST,
        weekdays: SeriesWeekdays = SeriesWeekdays.FULL_WEEK,
        calendar_merge_mode=CalendarMergeMode.AVAILABLE_IN_ANY,
        currency="",
        start_point: "StartOrEndPoint" = None,
        end_point: "StartOrEndPoint" = None,
        raise_error: bool = None
    ) -> SeriesMethods.GetUnifiedSeriesReturn:
        def convert_to_unified_series_entry(
            entrie_or_name: Union[SeriesEntrie, str]
        ) -> "UnifiedSeriesEntry":
            if isinstance(entrie_or_name, str):
                entrie_or_name = SeriesEntrie(entrie_or_name)
            entrie = entrie_or_name
            return {
                "name": entrie.name,
                "missingValueMethod": entrie.missing_value_method,
                "partialPeriodsMethod": entrie.partial_periods_method,
                "toLowerFrequencyMethod": entrie.to_lowerfrequency_method,
                "toHigherFrequencyMethod": entrie.to_higherfrequency_method,
            }

        web_series_entries = list(map(convert_to_unified_series_entry, series_entries))

        request: "UnifiedSeriesRequest" = {
            "frequency": frequency,
            "weekdays": weekdays,
            "calendarMergeMode": calendar_merge_mode,
            "currency": currency,
            "seriesEntries": web_series_entries,
        }

        if start_point:
            request["startPoint"] = start_point.time
            request["startDateMode"] = start_point.mode

        if end_point:
            request["endPoint"] = end_point.time
            request["endDateMode"] = end_point.mode

        return _GetUnifiedSeriesReturn(
            self.__api.session,
            request,
            self.__api.raise_error if raise_error is None else raise_error,
        )
