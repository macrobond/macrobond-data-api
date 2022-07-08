# get_all_vintage_series_result


from typing import TYPE_CHECKING, Any, Dict, Sequence, List

from macrobond_financial.common.types import Series

from .._get_pandas import _get_pandas

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame  # type: ignore


class GetAllVintageSeriesResult(List[Series]):

    __slots__ = ("series_name",)

    series_name: str

    def __init__(
        self,
        series: Sequence[Series],
        series_name: str,
    ) -> None:
        super().__init__(series)
        self.series_name = series_name
        """series_name"""

    @property
    def series(self) -> List[Series]:
        """
        A sequence of the metadata of the entities found.
        """
        return list(self)

    def to_pd_data_frame(self) -> "DataFrame":
        pandas = _get_pandas()
        data = list(map(lambda s: s.values_to_pd_series(), self))
        data_frame = pandas.concat(data, axis=1, keys=[s.name for s in self])
        data_frame = data_frame.sort_index()
        return data_frame

    def to_dict(self) -> Dict[str, Any]:
        return {
            "series_name": self.series_name,
            "series": tuple(map(lambda x: x.to_dict(), self)),
        }

    def __repr__(self):
        return "GetAllVintageSeriesResult series_name: " + self.series_name
