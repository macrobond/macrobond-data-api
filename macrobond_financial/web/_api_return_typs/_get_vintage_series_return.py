# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, Tuple, cast, TYPE_CHECKING

from datetime import datetime

from macrobond_financial.common.api_return_typs import GetVintageSeriesReturn

from macrobond_financial.common.types import VintageSeries

from ._str_to_datetime import _str_to_datetime, _str_to_datetime_z


if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetVintageSeriesReturn(GetVintageSeriesReturn):
    def __init__(
        self,
        session: "Session",
        serie_name: str,
        time: datetime,
        _raise: bool,
    ) -> None:
        super().__init__(serie_name, time, _raise)
        self._session = session

    def _object(self) -> VintageSeries:
        response = self._session.series.fetch_vintage_series(
            self._time, self._serie_name, get_times_of_change=False
        )[0]

        error_message = response.get("errorText")
        if error_message:
            return VintageSeries(self._serie_name, error_message, None, None, None)

        metadata = cast(Dict[str, Any], response["metadata"])

        revision_time_stamp = cast(str, metadata.get("RevisionTimeStamp"))
        if not revision_time_stamp or self._time != _str_to_datetime_z(
            revision_time_stamp
        ):
            raise ValueError("Invalid time")

        values: Tuple[Optional[float], ...] = tuple(
            map(
                lambda x: float(x) if x else None,
                cast(List[Optional[float]], response["values"]),
            )
        )

        dates = tuple(map(_str_to_datetime, cast(List[str], response["dates"])))

        return VintageSeries(self._serie_name, None, metadata, values, dates)
