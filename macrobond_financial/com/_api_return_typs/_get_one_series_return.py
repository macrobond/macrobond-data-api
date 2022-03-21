# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

from macrobond_financial.common.typs import Series, GetEntitiesError

from macrobond_financial.common.api_return_typs import GetOneSeriesReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._series_helps import _create_series, _create_series_dicts

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..com_typs import (
        Database,
        Series as ComSeries,
    )

    from macrobond_financial.common.typs import (
        SeriesTypedDict,
    )


class _GetOneSeriesReturn(GetOneSeriesReturn):
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
