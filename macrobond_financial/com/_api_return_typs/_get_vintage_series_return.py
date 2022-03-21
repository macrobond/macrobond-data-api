# -*- coding: utf-8 -*-

from typing import Union, TYPE_CHECKING, cast

from datetime import datetime

from math import isnan

from macrobond_financial.common.api_return_typs import GetVintageSeriesReturn

from macrobond_financial.common.typs import VintageSeries, GetEntitiesError

from macrobond_financial.common._get_pandas import _get_pandas

from ._fill_metadata_from_entity import (
    _fill_metadata_from_entity,
    _copy_metadata_from_com_entity_cict,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..com_typs import Database, SeriesWithRevisions, Series as ComSeries
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

    from macrobond_financial.common.typs import VintageSeriesTypedDict


class _GetVintageSeriesReturn(GetVintageSeriesReturn):
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
