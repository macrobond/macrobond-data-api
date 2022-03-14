# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Tuple, Any, Union, Dict, List, TYPE_CHECKING

from macrobond_financial.common import (
    Entity,
    UnifiedSeries,
    UnifiedSerie,
    Series,
    GetEntitiesError,
    SeriesEntrie,
    CalendarMergeMode,
)
import macrobond_financial.common.series_methods as SeriesMethods
from macrobond_financial.common.enums import SeriesWeekdays, SeriesFrequency

from macrobond_financial.common._get_pandas import _get_pandas

from ._fill_metadata_from_entity import _fill_metadata_from_entity

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from .com_api import ComApi
    from .com_typs import (
        Connection,
        Database,
        SeriesRequest,
        Series as ComSeries,
        Entity as ComEntity,
    )

    from macrobond_financial.common import StartOrEndPoint
    from macrobond_financial.common.entity import EntityTypedDict
    from macrobond_financial.common.series import SeriesTypedDict
    from macrobond_financial.common.unified_series import (
        UnifiedSeriesDict,
        UnifiedSerieDict,
    )


def _create_entity(com_entity: "ComEntity", name: str) -> Entity:
    if com_entity.IsError:
        return Entity(name, com_entity.ErrorMessage, None)
    return Entity(name, None, _fill_metadata_from_entity(com_entity))


def _create_entity_dicts(com_entity: "ComEntity", name: str) -> "EntityTypedDict":
    if com_entity.IsError:
        return {
            "Name": name,
            "ErrorMessage": com_entity.ErrorMessage,
        }
    return {"Name": name, "MetaData": _fill_metadata_from_entity(com_entity)}


def _create_series(com_series: "ComSeries", name: str) -> Series:
    if com_series.IsError:
        return Series(name, com_series.ErrorMessage, None, None, None)
    return Series(
        name,
        None,
        _fill_metadata_from_entity(com_series),
        com_series.Values,
        com_series.DatesAtStartOfPeriod,
    )


def _create_series_dicts(com_series: "ComSeries", name: str) -> "SeriesTypedDict":
    if com_series.IsError:
        return {
            "Name": name,
            "ErrorMessage": com_series.ErrorMessage,
        }
    return {
        "Name": name,
        "Values": com_series.Values,
        "Dates": com_series.DatesAtStartOfPeriod,
        "MetaData": _fill_metadata_from_entity(com_series),
    }


class _GetOneSeriesReturn(SeriesMethods.GetOneSeriesReturn):
    def __init__(self, database: "Database", series_name: str, _raise: bool) -> None:
        self.__database = database
        self.__series_name = series_name
        self.__raise = _raise

    def fetch_one_series(self) -> "ComSeries":
        com_series = self.__database.FetchOneSeries(self.__series_name)
        if com_series.IsError and self.__raise:
            raise GetEntitiesError(self.__series_name, com_series.ErrorMessage)
        return com_series

    def object(self) -> Series:
        return _create_series(self.fetch_one_series(), self.__series_name)

    def dict(self) -> "SeriesTypedDict":
        return _create_series_dicts(self.fetch_one_series(), self.__series_name)

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        com_series = self.__database.FetchOneSeries(self.__series_name)

        if self.__raise and com_series.IsError:
            raise GetEntitiesError(self.__series_name, com_series.ErrorMessage)

        if com_series.IsError:
            error_series: "SeriesTypedDict" = {
                "Name": self.__series_name,
                "ErrorMessage": com_series.ErrorMessage,
            }
            kwargs["data"] = [error_series]
        else:
            series: "SeriesTypedDict" = {  # type: ignore
                "Values": com_series.Values,
                "Dates": com_series.DatesAtStartOfPeriod,
            }

            kwargs["data"] = series

        args = args[1:]
        return pandas.DataFrame(*args, **kwargs)


class _GetSeriesReturn(SeriesMethods.GetSeriesReturn):
    def __init__(
        self, database: "Database", series_names: Tuple[str, ...], _raise: bool
    ) -> None:
        self.__database = database
        self.__series_names = series_names
        self.__raise = _raise

    def fetch_series(self) -> Tuple["ComSeries", ...]:
        com_series = self.__database.FetchSeries(self.__series_names)
        GetEntitiesError.raise_if(
            self.__raise,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                self.__series_names,
                com_series,
            ),
        )
        return com_series

    def list_of_objects(self) -> List[Series]:
        return list(map(_create_series, self.fetch_series(), self.__series_names))

    def list_of_dicts(self) -> List["SeriesTypedDict"]:
        return list(map(_create_series_dicts, self.fetch_series(), self.__series_names))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetOneEntitieReturn(SeriesMethods.GetOneEntitieReturn):
    def __init__(self, database: "Database", entity_name: str, _raise: bool) -> None:
        self.__database = database
        self.__entity_name = entity_name
        self.__raise = _raise

    def fetch_one_entity(self) -> "ComEntity":
        com_entity = self.__database.FetchOneEntity(self.__entity_name)
        if self.__raise and com_entity.IsError:
            raise GetEntitiesError(self.__entity_name, com_entity.ErrorMessage)
        return com_entity

    def object(self) -> Entity:
        return _create_entity(self.fetch_one_entity(), self.__entity_name)

    def dict(self) -> "EntityTypedDict":
        return _create_entity_dicts(self.fetch_one_entity(), self.__entity_name)

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def metadata_as_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()

        entity = self.fetch_one_entity()
        return pandas.DataFrame.from_dict(
            _fill_metadata_from_entity(entity), orient="index", columns=["Attributes"]
        )


class _GetEntitiesReturn(SeriesMethods.GetEntitiesReturn):
    def __init__(
        self, database: "Database", entity_names: Tuple[str, ...], _raise: bool
    ) -> None:
        self.__database = database
        self.__entity_names = entity_names
        self.__raise = _raise

    def fetch_entities(self) -> Tuple["ComEntity", ...]:
        com_entitys = self.__database.FetchEntities(self.__entity_names)
        GetEntitiesError.raise_if(
            self.__raise,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                self.__entity_names,
                com_entitys,
            ),
        )
        return com_entitys

    def list_of_objects(self) -> List[Entity]:
        return list(map(_create_entity, self.fetch_entities(), self.__entity_names))

    def list_of_dicts(self) -> List["EntityTypedDict"]:
        return list(
            map(_create_entity_dicts, self.fetch_entities(), self.__entity_names)
        )

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)


class _GetUnifiedSeriesReturn(SeriesMethods.GetUnifiedSeriesReturn):
    def __init__(
        self, database: "Database", request: "SeriesRequest", _raise: bool
    ) -> None:
        super().__init__()
        self.__database = database
        self.__request = request
        self.__raise = _raise

    def fetch_series(self) -> Tuple["ComSeries", ...]:
        com_series = self.__database.FetchSeries(self.__request)

        GetEntitiesError.raise_if(
            self.__raise,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                map(lambda x: x.Name, self.__request.AddedSeries),
                com_series,
            ),
        )

        return com_series

    def object(self) -> UnifiedSeries:
        com_series = self.fetch_series()

        first = next(filter(lambda x: not x.IsError, com_series), None)
        dates = first.DatesAtStartOfPeriod if first else tuple()

        series: List[UnifiedSerie] = []

        for i, com_one_series in enumerate(com_series):
            name = self.__request.AddedSeries[i].Name
            if com_one_series.IsError:
                series.append(
                    UnifiedSerie(name, com_one_series.ErrorMessage, {}, tuple())
                )
            else:
                metadata: Dict[str, Any] = {}
                com_metadata = com_one_series.Metadata
                for names_and_description in com_metadata.ListNames():
                    metadata_name = names_and_description[0]
                    values = com_metadata.GetValues(metadata_name)
                    if len(values) == 1:
                        metadata[metadata_name] = values[0]
                    else:
                        metadata[metadata_name] = list(values)

                series.append(UnifiedSerie(name, "", metadata, com_one_series.Values))

        return UnifiedSeries(dates, tuple(series))

    def dict(self) -> "UnifiedSeriesDict":
        com_series = self.fetch_series()

        first = next(filter(lambda x: not x.IsError, com_series), None)
        dates = first.DatesAtStartOfPeriod if first else tuple()

        series: List["UnifiedSerieDict"] = []
        for i, com_one_series in enumerate(com_series):
            name = self.__request.AddedSeries[i].Name
            if com_one_series.IsError:
                series.append(
                    {
                        "error_message": com_one_series.ErrorMessage,
                        "name": name,
                        "metadata": {},
                        "values": tuple(),
                    }
                )
            else:
                metadata = {}
                com_metadata = com_one_series.Metadata
                for names_and_description in com_metadata.ListNames():
                    metadata_name = names_and_description[0]
                    values = com_metadata.GetValues(metadata_name)
                    if len(values) == 1:
                        metadata[metadata_name] = values[0]
                    else:
                        metadata[metadata_name] = list(values)

                series.append(
                    {
                        "error_message": "",
                        "name": name,
                        "values": com_one_series.Values,
                        "metadata": metadata,
                    }
                )

        return {"dates": dates, "series": tuple(series)}

    def data_frame(self, columns: List[str] = None) -> "DataFrame":
        pandas = _get_pandas()
        com_series = self.fetch_series()
        data: Dict[str, Any] = OrderedDict()

        first = next(filter(lambda x: not x.IsError, com_series), None)
        if first:
            dates_name = "dates" if not columns else columns[0]
            data[dates_name] = first.DatesAtStartOfPeriod

        for i, com_one_series in enumerate(com_series):
            if not com_one_series.IsError:
                name = columns[i + 1] if columns else self.__request.AddedSeries[i].Name
                data[name] = com_one_series.Values

        return pandas.DataFrame.from_dict(data)


class _ComSeriesMethods(SeriesMethods.SeriesMethods):
    def __init__(self, api: "ComApi") -> None:
        super().__init__()
        self.__api = api

    def get_one_series(
        self, series_name: str, raise_error: bool = None
    ) -> SeriesMethods.GetOneSeriesReturn:
        return _GetOneSeriesReturn(
            self.__api.connection.Database,
            series_name,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_series(
        self, *series_names: str, raise_error: bool = None
    ) -> SeriesMethods.GetSeriesReturn:
        return _GetSeriesReturn(
            self.__api.connection.Database,
            series_names,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_one_entitie(
        self, entity_name: str, raise_error: bool = None
    ) -> SeriesMethods.GetOneEntitieReturn:
        return _GetOneEntitieReturn(
            self.__api.connection.Database,
            entity_name,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_entities(
        self, *entity_names: str, raise_error: bool = None
    ) -> SeriesMethods.GetEntitiesReturn:
        return _GetEntitiesReturn(
            self.__api.connection.Database,
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
        request = self.__api.connection.Database.CreateUnifiedSeriesRequest()
        for entrie_or_name in series_entries:
            if isinstance(entrie_or_name, str):
                entrie_or_name = SeriesEntrie(entrie_or_name)

            entrie = entrie_or_name
            series_expression = request.AddSeries(entrie.name)

            series_expression.MissingValueMethod = entrie.missing_value_method

            series_expression.ToLowerFrequencyMethod = entrie.to_lowerfrequency_method

            series_expression.ToHigherFrequencyMethod = (
                entrie_or_name.to_higherfrequency_method
            )

            series_expression.PartialPeriodsMethod = (
                entrie_or_name.partial_periods_method
            )

        request.Frequency = frequency

        request.Weekdays = weekdays

        request.CalendarMergeMode = calendar_merge_mode

        request.Currency = currency

        if start_point:
            request.StartDate = start_point.time
            request.StartDateMode = start_point.mode

        if end_point:
            request.EndDate = end_point.time
            request.EndDateMode = end_point.mode

        return _GetUnifiedSeriesReturn(
            self.__api.connection.Database,
            request,
            self.__api.raise_error if raise_error is None else raise_error,
        )
