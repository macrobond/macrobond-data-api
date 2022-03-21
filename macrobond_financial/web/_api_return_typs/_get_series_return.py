# -*- coding: utf-8 -*-

# pylint: disable = missing-module-docstring

from typing import Sequence, List, TYPE_CHECKING
from macrobond_financial.common.typs import Series, GetEntitiesError

from macrobond_financial.common.api_return_typs import GetSeriesReturn

from macrobond_financial.common._get_pandas import _get_pandas

from ._series_helps import _create_series, _create_series_dicts

if TYPE_CHECKING:  # pragma: no cover
    from ..session import Session
    from pandas import DataFrame  # type: ignore

    from macrobond_financial.common.typs import SeriesTypedDict

    from ..web_typs import SeriesResponse


class _GetSeriesReturn(GetSeriesReturn):
    def __init__(
        self, session: "Session", series_names: Sequence[str], _raise: bool
    ) -> None:
        self._session = session
        self._series_names = series_names
        self._raise = _raise

    def fetch_series(self) -> List["SeriesResponse"]:
        response = self._session.series.fetch_series(*self._series_names)
        GetEntitiesError.raise_if(
            self._raise,
            map(lambda x, y: (x, y.get("errorText")), self._series_names, response),
        )
        return response

    def list_of_objects(self) -> List[Series]:
        response = self.fetch_series()
        return list(map(_create_series, response, self._series_names))

    def list_of_dicts(self) -> List["SeriesTypedDict"]:
        response = self.fetch_series()
        return list(map(_create_series_dicts, response, self._series_names))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.list_of_dicts()
        return pandas.DataFrame(*args, **kwargs)
