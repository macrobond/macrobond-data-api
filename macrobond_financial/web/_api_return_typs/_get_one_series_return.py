# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Tuple, List, Optional, cast, TYPE_CHECKING

from datetime import datetime, timezone

from macrobond_financial.common.typs import Series, GetEntitiesError

from macrobond_financial.common.api_return_typs import GetOneSeriesReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._series_helps import _create_series, _create_series_dicts

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from ..web_typs import SeriesResponse
    from pandas import DataFrame  # type: ignore

    from macrobond_financial.common.typs import SeriesTypedDict


class _GetOneSeriesReturn(GetOneSeriesReturn):
    def __init__(self, session: "Session", series_name: str, _raise: bool) -> None:
        self._session = session
        self._series_name = series_name
        self._raise = _raise

    def fetch_series(self) -> "SeriesResponse":
        response = self._session.series.fetch_series(self._series_name)[0]
        GetEntitiesError.raise_if(
            self._raise, self._series_name, response.get("errorText")
        )
        return response

    def object(self) -> Series:
        return _create_series(self.fetch_series(), self._series_name)

    def dict(self) -> "SeriesTypedDict":
        return _create_series_dicts(self.fetch_series(), self._series_name)

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = [self.dict()]
        return pandas.DataFrame(*args, **kwargs)

    def values_and_dates_as_data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        response = self.fetch_series()
        error_text = response.get("errorText")

        if error_text:
            error_series: "SeriesTypedDict" = {
                "Name": self._series_name[0],
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
