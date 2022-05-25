# -*- coding: utf-8 -*-


from datetime import datetime

from typing import TYPE_CHECKING, Any, Dict, List, Union, overload, Sequence, Tuple
from abc import ABC, abstractmethod

from ..types import SeriesObservationHistory, SeriesObservationHistoryColumns

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class GetObservationHistoryReturn(ABC):
    def __init__(self, serie_name: str, times: Sequence[datetime]) -> None:
        self._serie_name = serie_name
        self._times = times

    @abstractmethod
    def object(self) -> Tuple[SeriesObservationHistory, ...]:
        ...

    def dict(self) -> List[Dict[str, Any]]:
        return list(map(lambda x: x.to_dict(), self.object()))

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union[SeriesObservationHistoryColumns, "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.dict()
        return pandas.DataFrame(*args, **kwargs)
