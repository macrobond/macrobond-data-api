# -*- coding: utf-8 -*-


from typing import TYPE_CHECKING, Sequence, Tuple
from datetime import datetime

from macrobond_financial.common.api_return_types import (
    GetObservationHistoryReturn,
)
from macrobond_financial.common.types import SeriesObservationHistory

from ._str_to_datetime import _str_to_datetime, _optional_str_to_datetime_z

from ..session import SessionHttpException

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetObservationHistoryReturn(GetObservationHistoryReturn):
    def __init__(
        self, session: "Session", serie_name: str, times: Sequence[datetime]
    ) -> None:
        super().__init__(serie_name, times)
        self._session = session

    def object(self) -> Tuple[SeriesObservationHistory, ...]:
        try:
            response = self._session.series.fetch_observation_history(
                self._serie_name, list(self._times)
            )
        except SessionHttpException as ex:
            if ex.status_code == 404:
                raise Exception(ex.response.json()["detail"]) from ex
            raise ex

        return tuple(
            map(
                lambda x: SeriesObservationHistory(
                    _str_to_datetime(x["observationDate"]),
                    tuple(map(lambda v: float(v) if v else None, x["values"])),
                    tuple(map(_optional_str_to_datetime_z, x["timeStamps"])),
                ),
                response,
            )
        )
