# -*- coding: utf-8 -*-

from typing import Any, Dict, List, TYPE_CHECKING

from math import isnan

from macrobond_financial.common.types import UnifiedSeries, UnifiedSerie
from macrobond_financial.common.api_return_types import GetUnifiedSeriesReturn

if TYPE_CHECKING:  # pragma: no cover
    from ..com_types import Database, SeriesRequest


class _GetUnifiedSeriesReturn(GetUnifiedSeriesReturn):
    def __init__(
        self, database: "Database", request: "SeriesRequest", _raise: bool
    ) -> None:
        super().__init__(_raise)
        self.__database = database
        self.__request = request

    def _object(self) -> UnifiedSeries:
        com_series = self.__database.FetchSeries(self.__request)

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

                series.append(
                    UnifiedSerie(
                        name,
                        "",
                        metadata,
                        tuple(
                            map(
                                lambda x: None if x is not None and isnan(x) else x,
                                com_one_series.Values,
                            )
                        ),
                    )
                )

        return UnifiedSeries(dates, tuple(series))
