# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING
from macrobond_financial.common.api_return_types import GetNthReleaseReturn

from macrobond_financial.common.types import Series

from ._series_helps import _create_series


if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session


class _GetNthReleaseReturn(GetNthReleaseReturn):
    def __init__(
        self,
        session: "Session",
        series_name: str,
        nth: int,
        _raise: bool,
    ) -> None:
        super().__init__(series_name, nth, _raise)
        self._session = session

    def _object(self) -> Series:
        response = self._session.series.fetch_nth_release_series(
            self._nth, self._series_name
        )[0]
        return _create_series(response, self._series_name)
