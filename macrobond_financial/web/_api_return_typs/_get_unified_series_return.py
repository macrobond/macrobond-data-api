# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Any, Dict, List, Optional, cast, TYPE_CHECKING

from macrobond_financial.common.types import UnifiedSeries, UnifiedSerie
from macrobond_financial.common.api_return_types import GetUnifiedSeriesReturn

from ._str_to_datetime import _str_to_datetime

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from ..web_types import UnifiedSeriesRequest


class _GetUnifiedSeriesReturn(GetUnifiedSeriesReturn):
    def __init__(
        self, session: "Session", request: "UnifiedSeriesRequest", _raise: bool
    ) -> None:
        super().__init__(_raise)
        self._session = session
        self._request = request

    def _object(self) -> UnifiedSeries:
        response = self._session.series.fetch_unified_series(self._request)

        str_dates = response.get("dates")
        if str_dates:
            dates = tuple(map(_str_to_datetime, str_dates))
        else:
            dates = tuple()

        series: List[UnifiedSerie] = []
        for i, one_series in enumerate(response["series"]):
            name = self._request["seriesEntries"][i]["name"]
            error_text = one_series.get("errorText")

            if error_text:
                series.append(UnifiedSerie(name, error_text, {}, tuple()))
            else:
                values = tuple(
                    map(
                        lambda x: float(x) if x else None,
                        cast(List[Optional[float]], one_series["values"]),
                    )
                )
                metadata = cast(Dict[str, Any], one_series["metadata"])
                series.append(UnifiedSerie(name, "", metadata, values))

        return UnifiedSeries(dates, tuple(series))
