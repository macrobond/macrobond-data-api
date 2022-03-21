# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Tuple, Any, Dict, List, TYPE_CHECKING

from macrobond_financial.common.typs import (
    UnifiedSeries,
    UnifiedSerie,
    GetEntitiesError,
)
from macrobond_financial.common.api_return_typs import GetUnifiedSeriesReturn

from macrobond_financial.common._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore
    from ..com_typs import Database, SeriesRequest, Series as ComSeries

    from macrobond_financial.common.typs.unified_series import (
        UnifiedSeriesDict,
        UnifiedSerieDict,
    )


class _GetUnifiedSeriesReturn(GetUnifiedSeriesReturn):
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
