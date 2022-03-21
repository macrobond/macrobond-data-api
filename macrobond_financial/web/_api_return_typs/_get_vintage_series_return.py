# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, cast, TYPE_CHECKING

from datetime import datetime

from macrobond_financial.common.api_return_typs import (
    GetVintageSeriesReturn,
)

from macrobond_financial.common.typs import GetEntitiesError, VintageSeries

from macrobond_financial.common._get_pandas import _get_pandas

from ._copy_metadata import _copy_metadata

from ._str_to_datetime import _str_to_datetime_z, _str_to_datetime


if TYPE_CHECKING:  # pragma: no cover

    from macrobond_financial.common.typs import VintageSeriesTypedDict

    from ..web_typs import VintageSeriesResponse
    from ..session import Session
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class _GetVintageSeriesReturn(GetVintageSeriesReturn):
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
