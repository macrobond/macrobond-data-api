# -*- coding: utf-8 -*-

from typing import Tuple, List, TYPE_CHECKING

from macrobond_financial.common.typs import (
    Series,
    GetEntitiesError,
)
from macrobond_financial.common.api_return_typs import GetSeriesReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._series_helps import _create_series, _create_series_dicts

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..com_typs import (
        Database,
        Series as ComSeries,
    )

    from macrobond_financial.common.typs import SeriesTypedDict


class _GetSeriesReturn(GetSeriesReturn):
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
