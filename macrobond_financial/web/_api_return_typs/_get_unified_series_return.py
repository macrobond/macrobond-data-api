# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from collections import OrderedDict
from typing import Any, Dict, Tuple, List, Optional, cast, TYPE_CHECKING

from datetime import datetime, timezone

from macrobond_financial.common.typs import (
    UnifiedSeries,
    UnifiedSerie,
    GetEntitiesError,
)

from macrobond_financial.common.api_return_typs import GetUnifiedSeriesReturn

from macrobond_financial.common._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from pandas import DataFrame  # type: ignore

    from macrobond_financial.common.typs import (
        UnifiedSeriesDict,
        UnifiedSerieDict,
    )

    from ..web_typs import UnifiedSeriesRequest, UnifiedSeriesResponse


class _GetUnifiedSeriesReturn(GetUnifiedSeriesReturn):
    def __init__(
        self, session: "Session", request: "UnifiedSeriesRequest", _raise: bool
    ) -> None:
        super().__init__()
        self._session = session
        self._request = request
        self._raise = _raise

    def fetch_unified_series(self) -> "UnifiedSeriesResponse":
        response = self._session.series.fetch_unified_series(self._request)

        GetEntitiesError.raise_if(
            self._raise,
            map(
                lambda x, y: (x["name"], y.get("errorText")),
                self._request["seriesEntries"],
                response["series"],
            ),
        )
        return response

    @classmethod
    def get_dates(cls, response: "UnifiedSeriesResponse") -> Tuple[datetime, ...]:
        str_dates = response.get("dates")
        if str_dates:
            return tuple(
                map(
                    lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").replace(
                        tzinfo=timezone.utc
                    ),
                    cast(List[str], str_dates),
                )
            )
        return tuple()

    def object(self) -> UnifiedSeries:
        response = self.fetch_unified_series()

        dates = self.get_dates(response)

        series: List[UnifiedSerie] = []
        for i, one_series in enumerate(response["series"]):
            name = self._request["seriesEntries"][i]["name"]
            error_text = one_series.get("errorText")

            if error_text:
                series.append(UnifiedSerie(name, error_text, {}, tuple()))
            else:
                values = cast(Tuple[Optional[float]], one_series["values"])
                metadata = cast(Dict[str, Any], one_series["metadata"])
                series.append(UnifiedSerie(name, "", metadata, values))

        return UnifiedSeries(dates, tuple(series))

    def dict(self) -> "UnifiedSeriesDict":
        response = self.fetch_unified_series()
        dates = self.get_dates(response)
        series: List["UnifiedSerieDict"] = []
        for i, one_series in enumerate(response["series"]):
            name = self._request["seriesEntries"][i]["name"]
            error_text = one_series.get("errorText")
            if error_text:
                series.append(
                    {
                        "error_message": error_text,
                        "name": name,
                        "metadata": {},
                        "values": tuple(),
                    }
                )
            else:
                values = cast(Tuple[Optional[float]], one_series["values"])
                metadata = cast(Dict[str, Any], one_series["metadata"])
                series.append(
                    {
                        "error_message": "",
                        "name": name,
                        "values": values,
                        "metadata": metadata,
                    }
                )
        return {"dates": dates, "series": tuple(series)}

    def data_frame(self, columns: List[str] = None) -> "DataFrame":
        pandas = _get_pandas()
        response = self.fetch_unified_series()
        data: Dict[str, Any] = OrderedDict()

        dates_name = "dates" if not columns else columns[0]
        data[dates_name] = self.get_dates(response)

        for i, one_series in enumerate(response["series"]):
            if not one_series.get("errorText"):
                name = (
                    columns[i + 1]
                    if columns
                    else self._request["seriesEntries"][i]["name"]
                )
                data[name] = cast(Tuple[Optional[float]], one_series["values"])

        return pandas.DataFrame.from_dict(data)
