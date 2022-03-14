# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Sequence, Optional, cast, TYPE_CHECKING

from datetime import datetime, timezone

import macrobond_financial.common.revision_methods as RevisionMethods

from macrobond_financial.common.get_entitie_error import GetEntitiesError

from macrobond_financial.common._get_pandas import _get_pandas

from macrobond_financial.common.vintage_series import VintageSeries
from macrobond_financial.common.series import Series

from ._copy_metadata import _copy_metadata

if TYPE_CHECKING:  # pragma: no cover
    from .web_typs.series_with_revisions_info_response import (
        SeriesWithRevisionsInfoResponse,
    )

    from macrobond_financial.common.vintage_series import VintageSeriesTypedDict
    from macrobond_financial.common.series import SeriesTypedDict

    from .web_typs.vintage_series_response import VintageSeriesResponse
    from .web_typs.series_observation_history_response import (
        SeriesObservationHistoryResponse,
    )
    from .web_api import WebApi
    from .session import Session
    from macrobond_financial.common.revision_methods import RevisionInfoDict
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


def _str_to_datetime_z(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc
    )


def _optional_str_to_datetime_z(datetime_str: Optional[str]) -> Optional[datetime]:
    return _str_to_datetime_z(datetime_str) if datetime_str else None


def _str_to_datetime(datetime_str: str) -> datetime:
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S").replace(
        tzinfo=timezone.utc
    )


def _optional_str_to_datetime(datetime_str: Optional[str]) -> Optional[datetime]:
    return _str_to_datetime(datetime_str) if datetime_str else None


class _GetRevisionInfoReturn(RevisionMethods.GetRevisionInfoReturn):
    def __init__(
        self,
        session: "Session",
        series_names: Sequence[str],
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__session = session
        self.__series_names = series_names
        self.__raise_error = raise_error

    def get_revision_info(self) -> List["SeriesWithRevisionsInfoResponse"]:
        response = self.__session.series.get_revision_info(*self.__series_names)

        GetEntitiesError.raise_if(
            self.__raise_error,
            map(lambda x, y: (x, y.get("errorText")), self.__series_names, response),
        )

        return response

    def object(self) -> List[RevisionMethods.RevisionInfo]:
        def to_obj(name: str, serie: "SeriesWithRevisionsInfoResponse"):
            error_text = serie.get("errorText")
            if error_text:
                return RevisionMethods.RevisionInfo(
                    name,
                    error_text,
                    False,
                    False,
                    None,
                    None,
                    tuple(),
                )

            time_stamp_of_first_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfFirstRevision")
            )

            time_stamp_of_last_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfLastRevision")
            )

            vintage_time_stamps = tuple(
                map(
                    _str_to_datetime_z,
                    serie["vintageTimeStamps"],
                )
            )

            return RevisionMethods.RevisionInfo(
                name,
                "",
                serie["storesRevisions"],
                serie["hasRevisions"],
                time_stamp_of_first_revision,
                time_stamp_of_last_revision,
                vintage_time_stamps,
            )

        return list(map(to_obj, self.__series_names, self.get_revision_info()))

    def dict(self) -> List["RevisionInfoDict"]:
        def to_dict(
            name: str, serie: "SeriesWithRevisionsInfoResponse"
        ) -> "RevisionInfoDict":
            error_text = serie.get("errorText")
            if error_text:
                return {
                    "name": name,
                    "error_message": error_text,
                }

            time_stamp_of_first_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfFirstRevision")
            )

            time_stamp_of_last_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfLastRevision")
            )

            vintage_time_stamps = tuple(
                map(
                    _str_to_datetime_z,
                    serie["vintageTimeStamps"],
                )
            )

            return {
                "name": name,
                "stores_revisions": serie["storesRevisions"],
                "has_revisions": serie["hasRevisions"],
                "time_stamp_of_first_revision": time_stamp_of_first_revision,
                "time_stamp_of_last_revision": time_stamp_of_last_revision,
                "vintage_time_stamps": vintage_time_stamps,
            }

        return list(map(to_dict, self.__series_names, self.get_revision_info()))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.dict()
        return pandas.DataFrame(*args, **kwargs)


class _GetVintageSeriesReturn(RevisionMethods.GetVintageSeriesReturn):
    def __init__(
        self,
        session: "Session",
        serie_name: str,
        time: datetime,
        raise_error: bool,
    ) -> None:
        super().__init__()
        self._session = session
        self._serie_name = serie_name
        self._time = time
        self._raise_error = raise_error

    def fetch_vintage_series(self) -> "VintageSeriesResponse":
        response = self._session.series.fetch_vintage_series(
            self._time, self._serie_name, get_times_of_change=False
        )[0]

        GetEntitiesError.raise_if(
            self._raise_error, self._serie_name, response.get("errorText")
        )

        if not response.get("errorText"):
            revision_time_stamp_str = cast(Dict[str, Any], response["metadata"]).get(
                "RevisionTimeStamp"
            )
            if not revision_time_stamp_str or self._time != _str_to_datetime_z(
                revision_time_stamp_str
            ):
                raise ValueError("Invalid time")

        return response

    def object(self) -> VintageSeries:
        response = self.fetch_vintage_series()
        error_message = response.get("errorText")
        if error_message:
            return VintageSeries(self._serie_name, error_message, None, None, None)

        values = tuple(cast(List[Optional[float]], response["values"]))
        dates = tuple(map(_str_to_datetime, cast(List[str], response["dates"])))
        metadata = cast(Dict[str, Any], response["metadata"])

        return VintageSeries(self._serie_name, None, metadata, values, dates)

    def dict(self) -> "VintageSeriesTypedDict":
        response = self.fetch_vintage_series()
        error_message = response.get("errorText")
        if error_message:
            return {
                "Name": self._serie_name,
                "ErrorMessage": error_message,
            }
        values = tuple(cast(List[Optional[float]], response["values"]))
        dates = tuple(map(_str_to_datetime, cast(List[str], response["dates"])))
        metadata = cast(Dict[str, Any], response["metadata"])

        return {
            "Name": self._serie_name,
            "Values": values,
            "Dates": dates,
            "MetaData": metadata,
        }

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]

        response = self.fetch_vintage_series()
        error_message = response.get("errorText")
        if error_message:
            kwargs["data"] = [
                {
                    "Name": self._serie_name,
                    "ErrorMessage": error_message,
                }
            ]
        else:
            values = tuple(cast(List[Optional[float]], response["values"]))
            dates = tuple(map(_str_to_datetime, cast(List[str], response["dates"])))
            metadata = cast(Dict[str, Any], response["metadata"])

            kwargs["data"] = [
                _copy_metadata(
                    metadata,
                    {
                        "Name": self._serie_name,
                        "Values": values,
                        "Dates": dates,
                    },
                )
            ]

        return pandas.DataFrame(*args, **kwargs)


class _GetObservationHistoryReturn(RevisionMethods.GetObservationHistoryReturn):
    def __init__(
        self,
        session: "Session",
        serie_name: str,
        time: datetime,
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__session = session
        self.__serie_name = serie_name
        self.__time = time
        self.__raise_error = raise_error

    # def fetch_vintage_series(self) -> "SeriesObservationHistoryResponse":
    #    response = self.__session.series.fetch_observation_history(
    #        [self.__serie_name], [self.__time]
    #    )[0]
    #
    #    GetEntitiesError.raise_if(
    #        self.__raise_error, self.__serie_name, response.get("errorText")
    #    )
    #
    #    return response

    def object(self) -> Series:
        ...

    def dict(self) -> "SeriesTypedDict":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...


class _GetNthReleaseReturn(RevisionMethods.GetNthReleaseReturn):
    def __init__(
        self,
        session: "Session",
        serie_name: str,
        nth: int,
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__session = session
        self.__serie_name = serie_name
        self.__nth = nth
        self.__raise_error = raise_error

    def object(self) -> Series:
        ...

    def dict(self) -> "SeriesTypedDict":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...


class _WebRevisionMethods(RevisionMethods.RevisionMethods):
    def __init__(self, api: "WebApi") -> None:
        super().__init__()
        self.__api = api

    def get_revision_info(
        self, *series_names: str, raise_error: bool = None
    ) -> RevisionMethods.GetRevisionInfoReturn:
        return _GetRevisionInfoReturn(
            self.__api.session,
            series_names,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_vintage_series(
        self, serie_name: str, time: datetime, raise_error: bool = None
    ) -> RevisionMethods.GetVintageSeriesReturn:
        return _GetVintageSeriesReturn(
            self.__api.session,
            serie_name,
            time,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_observation_history(
        self, serie_name: str, time: datetime, raise_error: bool = None
    ) -> RevisionMethods.GetObservationHistoryReturn:
        return _GetObservationHistoryReturn(
            self.__api.session,
            serie_name,
            time,
            self.__api.raise_error if raise_error is None else raise_error,
        )

    def get_nth_release(
        self, serie_name: str, nth: int, raise_error: bool = None
    ) -> RevisionMethods.GetNthReleaseReturn:
        return _GetNthReleaseReturn(
            self.__api.session,
            serie_name,
            nth,
            self.__api.raise_error if raise_error is None else raise_error,
        )
