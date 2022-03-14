# -*- coding: utf-8 -*-

from ctypes import resize
from msilib.schema import Error
from typing import Sequence, Tuple, List, Union, TYPE_CHECKING, cast

from datetime import datetime

from math import isnan

import macrobond_financial.common.revision_methods as RevisionMethods

from macrobond_financial.common import VintageSeries, Series
from macrobond_financial.common.get_entitie_error import GetEntitiesError

from macrobond_financial.common._get_pandas import _get_pandas

from ._fill_metadata_from_entity import (
    _fill_metadata_from_entity,
    _copy_metadata_from_com_entity_cict,
)

if TYPE_CHECKING:  # pragma: no cover
    from macrobond_financial.common.revision_methods import RevisionInfoDict
    from .com_typs import Database, SeriesWithRevisions, Series as ComSeries
    from .com_api import ComApi
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

    from macrobond_financial.common import VintageSeriesTypedDict, SeriesTypedDict


class _GetRevisionInfoReturn(RevisionMethods.GetRevisionInfoReturn):
    def __init__(
        self,
        database: "Database",
        series_names: Sequence[str],
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__database = database
        self.__series_names = series_names
        self.__raise_error = raise_error

    def fetch_series_with_revisions(self) -> Tuple["SeriesWithRevisions", ...]:
        series = self.__database.FetchSeriesWithRevisions(self.__series_names)

        GetEntitiesError.raise_if(
            self.__raise_error,
            map(
                lambda x, y: (x, y.ErrorMessage if y.IsError else None),
                self.__series_names,
                series,
            ),
        )

        return series

    def object(self) -> List[RevisionMethods.RevisionInfo]:
        def to_obj(name: str, serie: "SeriesWithRevisions"):
            if serie.IsError:
                return RevisionMethods.RevisionInfo(
                    name,
                    serie.ErrorMessage,
                    False,
                    False,
                    None,
                    None,
                    tuple(),
                )

            vintage_time_stamps = tuple(serie.GetVintageDates())

            time_stamp_of_first_revision = (
                vintage_time_stamps[0] if serie.HasRevisions else None
            )
            time_stamp_of_last_revision = (
                vintage_time_stamps[-1] if serie.HasRevisions else None
            )

            return RevisionMethods.RevisionInfo(
                name,
                "",
                serie.StoresRevisions,
                serie.HasRevisions,
                time_stamp_of_first_revision,
                time_stamp_of_last_revision,
                vintage_time_stamps,
            )

        return list(
            map(to_obj, self.__series_names, self.fetch_series_with_revisions())
        )

    def dict(self) -> List["RevisionInfoDict"]:
        def to_dict(name: str, serie: "SeriesWithRevisions") -> "RevisionInfoDict":
            if serie.IsError:
                return {
                    "name": name,
                    "error_message": serie.ErrorMessage,
                }

            vintage_time_stamps = tuple(serie.GetVintageDates())

            time_stamp_of_first_revision = (
                vintage_time_stamps[0] if serie.HasRevisions else None
            )
            time_stamp_of_last_revision = (
                vintage_time_stamps[-1] if serie.HasRevisions else None
            )

            return {
                "name": name,
                "has_revisions": serie.HasRevisions,
                "stores_revisions": serie.StoresRevisions,
                "time_stamp_of_first_revision": time_stamp_of_first_revision,
                "time_stamp_of_last_revision": time_stamp_of_last_revision,
                "vintage_time_stamps": vintage_time_stamps,
            }

        return list(
            map(to_dict, self.__series_names, self.fetch_series_with_revisions())
        )

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.dict()
        return pandas.DataFrame(*args, **kwargs)


class _GetVintageSeriesReturn(RevisionMethods.GetVintageSeriesReturn):
    def __init__(
        self,
        database: "Database",
        serie_name: str,
        time: datetime,
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__database = database
        self.__serie_name = serie_name
        self.__time = time
        self.__raise_error = raise_error

    def get_vintage(self) -> Union["SeriesWithRevisions", "ComSeries"]:
        series_with_revisions = self.__database.FetchOneSeriesWithRevisions(
            self.__serie_name
        )

        if series_with_revisions.IsError:
            if self.__raise_error:
                raise GetEntitiesError(
                    self.__serie_name, series_with_revisions.ErrorMessage
                )
            return series_with_revisions

        try:
            series = series_with_revisions.GetVintage(self.__time)
        except OSError as os_error:
            if os_error.errno == 22 and os_error.strerror == "Invalid argument":
                raise ValueError("Invalid time") from os_error
            raise os_error

        if self.__raise_error and series.IsError:
            raise GetEntitiesError(self.__serie_name, series.ErrorMessage)

        return series

    def object(self) -> VintageSeries:
        series = self.get_vintage()
        if series.IsError:
            return VintageSeries(
                self.__serie_name,
                series.ErrorMessage,
                None,
                None,
                None,
            )

        series = cast("ComSeries", series)

        values = tuple(filter(lambda x: x is not None and not isnan(x), series.Values))
        dates = series.DatesAtStartOfPeriod[: len(values)]

        return VintageSeries(
            self.__serie_name,
            "",
            _fill_metadata_from_entity(series),
            values,
            dates,
        )

    def dict(self) -> "VintageSeriesTypedDict":
        series = self.get_vintage()
        if series.IsError:
            return {"Name": self.__serie_name, "ErrorMessage": series.ErrorMessage}

        series = cast("ComSeries", series)

        values = tuple(filter(lambda x: x is not None and not isnan(x), series.Values))
        dates = series.DatesAtStartOfPeriod[: len(values)]

        return {
            "Name": self.__serie_name,
            "Values": values,
            "Dates": dates,
            "MetaData": _fill_metadata_from_entity(series),
        }

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]

        series = self.get_vintage()
        if series.IsError:
            kwargs["data"] = [
                {"Name": self.__serie_name, "ErrorMessage": series.ErrorMessage}
            ]
        else:
            series = cast("ComSeries", series)

            values = tuple(
                filter(lambda x: x is not None and not isnan(x), series.Values)
            )
            dates = series.DatesAtStartOfPeriod[: len(values)]

            kwargs["data"] = [
                _copy_metadata_from_com_entity_cict(
                    series,
                    {"Name": self.__serie_name, "Values": values, "Dates": dates},
                )
            ]

        return pandas.DataFrame(*args, **kwargs)


class _GetObservationHistoryReturn(RevisionMethods.GetObservationHistoryReturn):
    def __init__(
        self,
        database: "Database",
        serie_name: str,
        time: datetime,
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__database = database
        self.__serie_name = serie_name
        self.__time = time
        self.__raise_error = raise_error

    def object(self) -> Series:
        ...

    def dict(self) -> "SeriesTypedDict":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...


class _GetNthReleaseReturn(RevisionMethods.GetNthReleaseReturn):
    def __init__(
        self,
        database: "Database",
        serie_name: str,
        nth: int,
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__database = database
        self.__serie_name = serie_name
        self.__nth = nth
        self.__raise_error = raise_error

    def object(self) -> Series:
        ...

    def dict(self) -> "SeriesTypedDict":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...


class _ComRevisionMethods(RevisionMethods.RevisionMethods):
    def __init__(self, api: "ComApi") -> None:
        super().__init__()
        self.__api = api

    def get_revision_info(
        self, *series_names: str, raise_error: bool = None
    ) -> RevisionMethods.GetRevisionInfoReturn:
        return _GetRevisionInfoReturn(
            self.__api.connection.Database,
            series_names,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_vintage_series(
        self, serie_name: str, time: datetime, raise_error: bool = None
    ) -> RevisionMethods.GetVintageSeriesReturn:
        return _GetVintageSeriesReturn(
            self.__api.connection.Database,
            serie_name,
            time,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_observation_history(
        self, serie_name: str, time: datetime, raise_error: bool = None
    ) -> RevisionMethods.GetObservationHistoryReturn:
        return _GetObservationHistoryReturn(
            self.__api.connection.Database,
            serie_name,
            time,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_nth_release(
        self, serie_name: str, nth: int, raise_error: bool = None
    ) -> RevisionMethods.GetNthReleaseReturn:
        return _GetNthReleaseReturn(
            self.__api.connection.Database,
            serie_name,
            nth,
            self.__api.raise_error if raise_error is None else raise_error,
        )
